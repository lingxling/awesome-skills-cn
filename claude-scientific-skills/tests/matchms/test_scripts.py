"""Tests for the matchms library-search helper.

`library_search.py` is a thin CLI over matchms, and almost everything that can
go wrong in it happens before or after the similarity calculation: the argument
validator that refuses pickle inputs and out-of-range thresholds, the
metric-name-to-class table that must cover every `--metric` choice the parser
advertises, the score-record reader that has to cope with both plain floats and
matchms' structured `(score, matches)` records, and `write_hits`, where the
top-k / min-score / min-matches decisions are actually made.

Those groups are driven directly. The metric table and the score-record reader
guard the two silent-wrong-answer failure modes -- a `--metric` the parser
accepts but `create_metric` cannot build, and a structured record read as a
scalar so `matched_peaks` is dropped. The end-to-end test then searches a
spectrum against a library containing a copy of itself, where cosine similarity
is exactly 1.0 by construction, so it pins the whole pipeline to a value that
is right independently of this code.
"""

from __future__ import annotations

import argparse
import csv
import sys
import tempfile
import unittest
from pathlib import Path

import pytest

import skill_contract

SKILL_ROOT = Path(__file__).resolve().parents[2] / "skills" / "matchms"
SCRIPTS = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

pytest.importorskip("matchms", reason="matchms skill needs matchms")
numpy = pytest.importorskip("numpy", reason="matchms skill needs numpy")

from matchms import similarity as matchms_similarity  # noqa: E402
from matchms.similarity.BaseSimilarity import BaseSimilarity  # noqa: E402

import library_search  # noqa: E402

CliHelpTests = skill_contract.cli.help_test_case(SKILL_ROOT)

#: A five-peak MGF spectrum. Five peaks is the minimum `--min-peaks` default
#: accepts, and the intensities stay above the 1% relative cutoff.
QUERY_MGF = """BEGIN IONS
TITLE=alpha
PEPMASS=350.1
CHARGE=1+
100.0000 100.0
150.0000 50.0
200.0000 30.0
250.0000 20.0
300.0000 10.0
END IONS
"""

#: Two references: a byte-for-byte copy of the query, and a spectrum sharing no
#: fragment with it.
LIBRARY_MGF = """BEGIN IONS
TITLE=alpha_copy
PEPMASS=350.1
CHARGE=1+
100.0000 100.0
150.0000 50.0
200.0000 30.0
250.0000 20.0
300.0000 10.0
END IONS

BEGIN IONS
TITLE=alpha_twin
PEPMASS=350.1
CHARGE=1+
100.0000 100.0
150.0000 50.0
200.0000 30.0
250.0000 20.0
300.0000 10.0
END IONS

BEGIN IONS
TITLE=unrelated
PEPMASS=500.2
CHARGE=1+
111.0000 100.0
161.0000 50.0
211.0000 30.0
261.0000 20.0
311.0000 10.0
END IONS
"""


def metric_choices() -> list[str]:
    """The `--metric` values the parser advertises.

    argparse exposes no public accessor for a choice list, so this reads the
    action table; the alternative is duplicating the list here, which is
    exactly the drift the tests below exist to catch.
    """
    for action in library_search.build_parser()._actions:
        if action.dest == "metric":
            return list(action.choices)
    raise AssertionError("the parser no longer defines --metric")


def score_record(score: float, matches: int):
    """One matchms-style structured score record."""
    dtype = [("Fake_score", "<f8"), ("Fake_matches", "<i8")]
    return numpy.array([(score, matches)], dtype=dtype)[0]


class FakeSpectrum:
    """Stands in for a matchms Spectrum: metadata lookup and nothing else."""

    def __init__(self, **metadata) -> None:
        self._metadata = metadata

    def get(self, key):
        return self._metadata.get(key)


class FakeScores:
    """Stands in for matchms Scores with a fixed, hand-chosen ranking."""

    score_names = ("Fake_score", "Fake_matches")

    def __init__(self, ranked) -> None:
        self.ranked = ranked
        self.requested_name = None
        self.requested_sort = None

    def scores_by_query(self, query, name, sort):
        self.requested_name = name
        self.requested_sort = sort
        return self.ranked


def search_namespace(**overrides) -> argparse.Namespace:
    """A namespace with every default `build_parser` would produce."""
    defaults = dict(
        queries=None,
        references=None,
        output=None,
        metric="modified",
        tolerance=0.02,
        top_k=10,
        min_score=0.0,
        min_matches=0,
        array_type="numpy",
        max_pairs=5_000_000,
        relative_intensity=0.01,
        min_peaks=5,
        max_peaks=None,
        mz_min=None,
        mz_max=None,
        remove_precursor_window=None,
        no_default_filters=False,
        no_normalize=False,
        query_id_field=None,
        reference_id_field=None,
        bin_width=0.001,
        blink_top_k=None,
        force=False,
        quiet=True,
    )
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


class MetricTableTests(unittest.TestCase):
    """`create_metric` must cover every metric the parser accepts."""

    def test_every_advertised_metric_builds_a_similarity_object(self) -> None:
        # A choice the parser accepts but create_metric cannot build would only
        # fail after both spectrum files have been loaded and processed.
        for name in metric_choices():
            with self.subTest(metric=name):
                metric = library_search.create_metric(search_namespace(metric=name))
                self.assertIsInstance(metric, BaseSimilarity)

    def test_each_metric_name_selects_the_documented_matchms_class(self) -> None:
        expected = {
            "cosine": matchms_similarity.CosineGreedy,
            "cosine-exact": matchms_similarity.CosineHungarian,
            "cosine-linear": matchms_similarity.CosineLinear,
            "modified": matchms_similarity.ModifiedCosineGreedy,
            "modified-exact": matchms_similarity.ModifiedCosineHungarian,
            "neutral-loss": matchms_similarity.NeutralLossesCosine,
            "blink": matchms_similarity.BlinkCosine,
        }
        # Every non-flash choice is covered, so a new metric cannot be added to
        # the parser without landing in this table.
        self.assertEqual(
            set(expected) | {"flash-entropy", "flash-cosine", "flash-modified"},
            set(metric_choices()),
        )
        for name, cls in expected.items():
            with self.subTest(metric=name):
                self.assertIsInstance(
                    library_search.create_metric(search_namespace(metric=name)), cls
                )

    def test_the_three_flash_metrics_differ_in_score_type_and_matching_mode(self) -> None:
        # All three build a FlashSimilarity; the distinction is entirely in the
        # constructor arguments, so a copy-paste slip would silently give the
        # user the wrong similarity.
        configurations = {
            name: library_search.create_metric(search_namespace(metric=name))
            for name in ("flash-entropy", "flash-cosine", "flash-modified")
        }
        self.assertEqual(
            {
                name: (metric.score_type, metric.matching_mode)
                for name, metric in configurations.items()
            },
            {
                "flash-entropy": ("spectral_entropy", "fragment"),
                "flash-cosine": ("cosine", "fragment"),
                # "modified" cosine means hybrid (precursor-shifted) matching.
                "flash-modified": ("cosine", "hybrid"),
            },
        )

    def test_an_unknown_metric_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported metric"):
            library_search.create_metric(search_namespace(metric="tanimoto"))

    def test_blink_receives_the_intensity_and_score_cutoffs(self) -> None:
        metric = library_search.create_metric(
            search_namespace(
                metric="blink", relative_intensity=0.02, blink_top_k=7, min_score=0.3
            )
        )
        self.assertEqual(metric.min_relative_intensity, 0.02)
        self.assertEqual(metric.top_k, 7)
        # BLINK prunes sparse scores itself; passing --min-score through avoids
        # materialising pairs the writer would drop anyway.
        self.assertEqual(metric.sparse_score_min, 0.3)

    def test_the_metric_sets_only_name_metrics_the_parser_offers(self) -> None:
        advertised = set(metric_choices())
        self.assertTrue(library_search.STRUCTURED_METRICS <= advertised)
        self.assertTrue(library_search.PRECURSOR_METRICS <= advertised)
        # Flash metrics report a score but no matched-peak count.
        self.assertEqual(
            library_search.STRUCTURED_METRICS
            & {"flash-entropy", "flash-cosine", "flash-modified"},
            set(),
        )


class SuffixPolicyTests(unittest.TestCase):
    def test_pickle_suffixes_are_never_also_supported(self) -> None:
        # Refusing pickles is a security decision; the two sets overlapping
        # would quietly re-enable arbitrary code execution on load.
        self.assertEqual(
            library_search.UNSAFE_PICKLE_SUFFIXES & library_search.SUPPORTED_SUFFIXES,
            set(),
        )

    def test_every_suffix_is_lowercase_and_dotted(self) -> None:
        # validate_args lowercases the suffix before the lookup, so an entry
        # spelled ".MGF" here would never match.
        for suffix in library_search.SUPPORTED_SUFFIXES | library_search.UNSAFE_PICKLE_SUFFIXES:
            with self.subTest(suffix=suffix):
                self.assertEqual(suffix, suffix.lower())
                self.assertTrue(suffix.startswith("."))


class ValidationTests(unittest.TestCase):
    """Both directions: a usable invocation passes, a broken one is named."""

    def setUp(self) -> None:
        self._temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary.cleanup)
        self.root = Path(self._temporary.name)
        self.queries = self.root / "queries.mgf"
        self.references = self.root / "library.msp"
        for path in (self.queries, self.references):
            path.write_text("", encoding="utf-8")
        self.output = self.root / "hits.csv"

    def args(self, **overrides) -> argparse.Namespace:
        settings = dict(
            queries=self.queries, references=self.references, output=self.output
        )
        settings.update(overrides)
        return search_namespace(**settings)

    def test_a_valid_invocation_passes_silently(self) -> None:
        # Without this the rest of the class only proves the validator can say
        # no -- not that it ever says yes.
        library_search.validate_args(self.args())

    def test_every_supported_suffix_is_accepted_in_both_positions(self) -> None:
        for suffix in sorted(library_search.SUPPORTED_SUFFIXES):
            with self.subTest(suffix=suffix):
                queries = self.root / f"q{suffix}"
                queries.write_text("", encoding="utf-8")
                library_search.validate_args(self.args(queries=queries))

    def test_uppercase_suffixes_are_accepted(self) -> None:
        queries = self.root / "queries.MGF"
        queries.write_text("", encoding="utf-8")
        library_search.validate_args(self.args(queries=queries))

    def test_a_missing_input_is_reported_by_role(self) -> None:
        for role, key in (("query", "queries"), ("reference", "references")):
            with self.subTest(role=role):
                with self.assertRaisesRegex(ValueError, f"{role} file does not exist"):
                    library_search.validate_args(
                        self.args(**{key: self.root / "absent.mgf"})
                    )

    def test_pickle_input_is_refused_with_the_reason(self) -> None:
        for name in ("library.pickle", "library.pkl"):
            with self.subTest(name=name):
                path = self.root / name
                path.write_bytes(b"")
                with self.assertRaisesRegex(ValueError, "unpickling can execute code"):
                    library_search.validate_args(self.args(references=path))

    def test_an_unsupported_suffix_lists_the_formats(self) -> None:
        path = self.root / "library.csv"
        path.write_text("", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "MGF, MSP, mzML, mzXML, or JSON"):
            library_search.validate_args(self.args(references=path))

    def test_an_existing_output_needs_force(self) -> None:
        self.output.write_text("", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "--force"):
            library_search.validate_args(self.args())
        # With --force the same invocation is fine.
        library_search.validate_args(self.args(force=True))

    def test_a_missing_output_directory_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "output directory does not exist"):
            library_search.validate_args(self.args(output=self.root / "no" / "hits.csv"))

    def test_numeric_bounds_are_enforced_at_the_boundary(self) -> None:
        cases = [
            ({"tolerance": 0.0}, "--tolerance must be positive"),
            ({"tolerance": -0.01}, "--tolerance must be positive"),
            ({"top_k": 0}, "--top-k must be positive"),
            ({"min_score": -0.001}, "--min-score must be between 0 and 1"),
            ({"min_score": 1.001}, "--min-score must be between 0 and 1"),
            ({"min_matches": -1}, "--min-matches cannot be negative"),
            ({"max_pairs": 0}, "--max-pairs must be positive"),
            ({"relative_intensity": 1.5}, "--relative-intensity must be between 0 and 1"),
            ({"min_peaks": -1}, "--min-peaks cannot be negative"),
            ({"max_peaks": 0}, "--max-peaks must be positive"),
            ({"remove_precursor_window": 0.0}, "--remove-precursor-window must be positive"),
            ({"bin_width": 0.0}, "--bin-width must be positive"),
            ({"blink_top_k": 0}, "--blink-top-k must be positive"),
        ]
        for overrides, message in cases:
            with self.subTest(**overrides):
                with self.assertRaisesRegex(ValueError, message):
                    library_search.validate_args(self.args(**overrides))

    def test_the_inclusive_ends_of_each_range_are_accepted(self) -> None:
        # 0 disables the peak filters and 0/1 are legal similarity scores, so
        # rejecting them would make documented invocations unusable.
        library_search.validate_args(
            self.args(min_score=0.0, min_peaks=0, relative_intensity=0.0)
        )
        library_search.validate_args(self.args(min_score=1.0, relative_intensity=1.0))

    def test_an_inverted_mz_window_is_refused_but_one_sided_is_fine(self) -> None:
        with self.assertRaisesRegex(ValueError, "--mz-min must be smaller"):
            library_search.validate_args(self.args(mz_min=500.0, mz_max=100.0))
        with self.assertRaisesRegex(ValueError, "--mz-min must be smaller"):
            library_search.validate_args(self.args(mz_min=100.0, mz_max=100.0))
        library_search.validate_args(self.args(mz_min=100.0))
        library_search.validate_args(self.args(mz_max=500.0))

    def test_min_matches_is_refused_for_metrics_that_report_no_matches(self) -> None:
        # Silently ignoring --min-matches would look like a filter that ran.
        with self.assertRaisesRegex(ValueError, "does not report matched-peak counts"):
            library_search.validate_args(self.args(metric="flash-entropy", min_matches=3))
        library_search.validate_args(self.args(metric="cosine", min_matches=3))
        # A zero threshold is a no-op, so it stays legal everywhere.
        library_search.validate_args(self.args(metric="flash-entropy", min_matches=0))


class ProcessingChainTests(unittest.TestCase):
    """`create_processor` decides which matchms filters run, and in what order."""

    @staticmethod
    def step_names(args: argparse.Namespace) -> list[str]:
        steps = library_search.create_processor(args).processing_steps
        return [step[0] if isinstance(step, tuple) else step for step in steps]

    def test_metadata_filters_run_before_the_peak_filters(self) -> None:
        # SpectrumProcessor keeps registered filters in their canonical order
        # but appends unknown callables; the script expands default_filters by
        # hand precisely so precursor m/z is derived before it is required.
        names = self.step_names(search_namespace(metric="modified"))
        self.assertLess(
            names.index("add_precursor_mz"), names.index("require_precursor_mz")
        )
        self.assertLess(
            names.index("normalize_intensities"),
            names.index("select_by_relative_intensity"),
        )
        self.assertEqual(names[-1], "require_minimum_number_of_peaks")

    def test_precursor_metrics_require_a_precursor_and_others_do_not(self) -> None:
        # A modified-cosine score is meaningless without precursor m/z, so the
        # requirement must switch on with the metric.
        for metric in sorted(library_search.PRECURSOR_METRICS):
            with self.subTest(metric=metric):
                self.assertIn(
                    "require_precursor_mz", self.step_names(search_namespace(metric=metric))
                )
        self.assertNotIn(
            "require_precursor_mz", self.step_names(search_namespace(metric="cosine"))
        )

    def test_a_precursor_window_forces_the_precursor_requirement(self) -> None:
        names = self.step_names(
            search_namespace(metric="cosine", remove_precursor_window=17.0)
        )
        self.assertIn("require_precursor_mz", names)
        self.assertIn("remove_peaks_around_precursor_mz", names)

    def test_the_optional_filters_are_absent_by_default(self) -> None:
        names = self.step_names(search_namespace(metric="cosine"))
        for absent in (
            "select_by_mz",
            "remove_peaks_around_precursor_mz",
            "reduce_to_number_of_peaks",
        ):
            with self.subTest(filter=absent):
                self.assertNotIn(absent, names)

    def test_each_switch_adds_exactly_its_own_filter(self) -> None:
        cases = [
            ({"mz_min": 50.0}, "select_by_mz"),
            ({"mz_max": 900.0}, "select_by_mz"),
            ({"max_peaks": 50}, "reduce_to_number_of_peaks"),
        ]
        for overrides, expected in cases:
            with self.subTest(**overrides):
                self.assertIn(expected, self.step_names(search_namespace(**overrides)))

    def test_the_disabling_flags_actually_remove_steps(self) -> None:
        self.assertNotIn(
            "normalize_intensities",
            self.step_names(search_namespace(no_normalize=True)),
        )
        self.assertNotIn(
            "add_compound_name",
            self.step_names(search_namespace(no_default_filters=True)),
        )

    def test_zero_thresholds_disable_their_filters(self) -> None:
        # `--relative-intensity 0` and `--min-peaks 0` are documented as "off",
        # not as "keep everything above zero".
        names = self.step_names(search_namespace(relative_intensity=0.0, min_peaks=0))
        self.assertNotIn("select_by_relative_intensity", names)
        self.assertNotIn("require_minimum_number_of_peaks", names)

    def test_the_same_chain_is_used_for_queries_and_references(self) -> None:
        # Comparing differently processed collections biases every score, so
        # the processor is built once from one namespace.
        args = search_namespace()
        self.assertEqual(self.step_names(args), self.step_names(args))


class ScoreRecordTests(unittest.TestCase):
    """matchms returns either a bare float or a structured `(score, matches)`."""

    def test_the_score_field_is_the_one_ending_in_score(self) -> None:
        self.assertEqual(
            library_search.choose_score_fields(
                ("CosineGreedy_matches", "CosineGreedy_score")
            ),
            ("CosineGreedy_score", "CosineGreedy_matches"),
        )

    def test_a_metric_without_a_score_suffix_falls_back_to_the_first_field(self) -> None:
        self.assertEqual(
            library_search.choose_score_fields(("FlashSimilarity",)),
            ("FlashSimilarity", None),
        )

    def test_a_structured_record_is_read_field_by_field(self) -> None:
        record = score_record(0.75, 9)
        self.assertEqual(library_search.numeric_field(record, "Fake_score"), 0.75)
        self.assertEqual(library_search.matched_peaks(record, "Fake_matches"), 9)

    def test_a_scalar_score_is_read_directly_and_reports_no_matches(self) -> None:
        self.assertEqual(library_search.numeric_field(numpy.float64(0.4), "Fake_score"), 0.4)
        # Flash metrics return a scalar; inventing a match count would be a lie.
        self.assertIsNone(library_search.matched_peaks(numpy.float64(0.4), "Fake_matches"))
        self.assertIsNone(library_search.matched_peaks(score_record(0.4, 3), None))

    def test_a_field_the_record_does_not_carry_is_not_invented(self) -> None:
        self.assertIsNone(library_search.matched_peaks(score_record(0.4, 3), "Other_matches"))


class SpectrumIdentityTests(unittest.TestCase):
    def test_the_preferred_field_wins_over_every_default(self) -> None:
        spectrum = FakeSpectrum(feature_id="F7", spectrum_id="S1", compound_name="caffeine")
        self.assertEqual(
            library_search.spectrum_id(
                spectrum, preferred="feature_id", index=3, prefix="query"
            ),
            "F7",
        )

    def test_the_default_order_prefers_spectrum_id_over_a_name(self) -> None:
        spectrum = FakeSpectrum(spectrum_id="S1", compound_name="caffeine", title="scan 4")
        self.assertEqual(
            library_search.spectrum_id(spectrum, preferred=None, index=3, prefix="query"),
            "S1",
        )

    def test_an_empty_value_is_skipped_rather_than_used(self) -> None:
        # An MGF with `TITLE=` yields "", which would produce a blank id column.
        spectrum = FakeSpectrum(spectrum_id="", id=None, compound_name="caffeine")
        self.assertEqual(
            library_search.spectrum_id(spectrum, preferred=None, index=3, prefix="query"),
            "caffeine",
        )

    def test_an_unidentified_spectrum_falls_back_to_prefix_and_index(self) -> None:
        self.assertEqual(
            library_search.spectrum_id(
                FakeSpectrum(), preferred=None, index=0, prefix="reference"
            ),
            "reference-0",
        )

    def test_a_numeric_identifier_is_stringified(self) -> None:
        self.assertEqual(
            library_search.spectrum_id(
                FakeSpectrum(scan_number=42), preferred=None, index=0, prefix="query"
            ),
            "42",
        )

    def test_missing_metadata_becomes_an_empty_cell_not_the_word_none(self) -> None:
        self.assertEqual(library_search.metadata_value(FakeSpectrum(), "inchikey"), "")
        self.assertEqual(
            library_search.metadata_value(FakeSpectrum(precursor_mz=350.1), "precursor_mz"),
            "350.1",
        )


class HitWritingTests(unittest.TestCase):
    """`write_hits` owns the top-k, min-score and min-matches decisions."""

    def setUp(self) -> None:
        self._temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary.cleanup)
        self.output = Path(self._temporary.name) / "hits.csv"
        self.references = [
            FakeSpectrum(spectrum_id="R0", compound_name="first", inchikey="AAA"),
            FakeSpectrum(spectrum_id="R1", compound_name="second"),
            FakeSpectrum(spectrum_id="R2", compound_name="third"),
        ]
        self.query = FakeSpectrum(spectrum_id="Q0", precursor_mz=350.1)

    def write(self, ranked, **overrides) -> list[dict[str, str]]:
        args = search_namespace(metric="cosine", **overrides)
        library_search.write_hits(
            self.output,
            scores=FakeScores(ranked),
            queries=[self.query],
            references=self.references,
            args=args,
        )
        with self.output.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))

    def ranked(self, *scores):
        return [
            (self.references[index], score_record(score, matches))
            for index, (score, matches) in enumerate(scores)
        ]

    def test_hits_are_numbered_from_one_and_carry_reference_metadata(self) -> None:
        rows = self.write(self.ranked((0.9, 8), (0.8, 6)))
        self.assertEqual([row["rank"] for row in rows], ["1", "2"])
        self.assertEqual([row["reference_index"] for row in rows], ["0", "1"])
        self.assertEqual([row["reference_id"] for row in rows], ["R0", "R1"])
        self.assertEqual(rows[0]["reference_compound_name"], "first")
        self.assertEqual(rows[0]["reference_inchikey"], "AAA")
        # Reference 1 has no inchikey; the cell must be empty, not "None".
        self.assertEqual(rows[1]["reference_inchikey"], "")
        self.assertEqual(rows[0]["query_id"], "Q0")
        self.assertEqual(rows[0]["metric"], "cosine")
        self.assertEqual(rows[0]["score_field"], "Fake_score")
        self.assertEqual(rows[0]["matched_peaks"], "8")

    def test_top_k_truncates_after_the_filters_not_before(self) -> None:
        # 0.4 is dropped by --min-score, so the third-ranked survivor must
        # still be reported when --top-k is 2.
        rows = self.write(
            self.ranked((0.9, 8), (0.4, 8), (0.7, 8)), min_score=0.5, top_k=2
        )
        self.assertEqual([row["score"] for row in rows], ["0.9", "0.7"])
        self.assertEqual([row["rank"] for row in rows], ["1", "2"])

    def test_a_score_exactly_at_the_threshold_is_kept(self) -> None:
        rows = self.write(self.ranked((0.5, 8)), min_score=0.5)
        self.assertEqual(len(rows), 1)
        rows = self.write(self.ranked((0.5, 8)), min_score=0.5000001)
        self.assertEqual(rows, [])

    def test_the_match_count_threshold_is_inclusive(self) -> None:
        self.assertEqual(len(self.write(self.ranked((0.9, 5)), min_matches=5)), 1)
        self.assertEqual(self.write(self.ranked((0.9, 4)), min_matches=5), [])

    def test_a_scalar_score_survives_a_match_threshold(self) -> None:
        # Metrics with no match count must not be filtered to nothing by a
        # threshold they cannot answer; validate_args already refuses that
        # combination, so write_hits must not silently drop the rows either.
        ranked = [(self.references[0], numpy.float64(0.9))]
        rows = self.write(ranked, min_matches=99)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["matched_peaks"], "")

    def test_a_non_finite_score_is_dropped(self) -> None:
        # A NaN comparison is neither above nor below the threshold, so it has
        # to be excluded explicitly or it would rank first after sorting.
        rows = self.write(self.ranked((float("nan"), 8), (0.6, 8)))
        self.assertEqual([row["score"] for row in rows], ["0.6"])
        self.assertEqual([row["rank"] for row in rows], ["1"])

    def test_an_empty_ranking_still_writes_a_header(self) -> None:
        self.assertEqual(self.write([]), [])
        first_line = self.output.read_text(encoding="utf-8").splitlines()[0]
        self.assertTrue(first_line.startswith("query_index,query_id"))

    def test_a_reference_outside_the_library_is_an_error_not_a_blank_row(self) -> None:
        stranger = FakeSpectrum(spectrum_id="X")
        with self.assertRaisesRegex(RuntimeError, "outside the input library"):
            self.write([(stranger, score_record(0.9, 8))])

    def test_the_writer_asks_for_a_sorted_ranking_by_the_score_field(self) -> None:
        scores = FakeScores(self.ranked((0.9, 8)))
        library_search.write_hits(
            self.output,
            scores=scores,
            queries=[self.query],
            references=self.references,
            args=search_namespace(),
        )
        # Ranks are assigned in iteration order, so the sort has to happen in
        # matchms rather than here.
        self.assertTrue(scores.requested_sort)
        self.assertEqual(scores.requested_name, "Fake_score")

    def test_scores_are_written_with_enough_precision_to_be_reproducible(self) -> None:
        rows = self.write(self.ranked((0.123456789012, 8)))
        self.assertEqual(rows[0]["score"], "0.123456789012")


class EndToEndSearchTests(unittest.TestCase):
    """A spectrum searched against a copy of itself scores exactly 1.0."""

    def setUp(self) -> None:
        self._temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary.cleanup)
        self.root = Path(self._temporary.name)
        self.queries = self.root / "queries.mgf"
        self.references = self.root / "library.mgf"
        self.queries.write_text(QUERY_MGF, encoding="utf-8")
        self.references.write_text(LIBRARY_MGF, encoding="utf-8")
        self.output = self.root / "hits.csv"

    def args(self, **overrides) -> argparse.Namespace:
        settings = dict(
            queries=self.queries,
            references=self.references,
            output=self.output,
            metric="cosine",
        )
        settings.update(overrides)
        return search_namespace(**settings)

    def rows(self) -> list[dict[str, str]]:
        with self.output.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))

    def test_an_identical_reference_is_reported_with_a_perfect_score(self) -> None:
        self.assertEqual(library_search.run(self.args()), 0)
        rows = self.rows()
        # Two of the three references are copies of the query; the third shares
        # no fragment, and matchms stores no entry for a zero score.
        self.assertEqual(len(rows), 2)
        for row in rows:
            self.assertEqual(float(row["score"]), 1.0)
            # All five peaks match within the 0.02 Da tolerance.
            self.assertEqual(row["matched_peaks"], "5")
            self.assertEqual(row["query_id"], "alpha")
            self.assertEqual(row["query_precursor_mz"], "350.1")
        self.assertEqual(
            sorted(row["reference_id"] for row in rows), ["alpha_copy", "alpha_twin"]
        )

    def test_top_k_limits_the_reported_hits(self) -> None:
        self.assertEqual(library_search.run(self.args(top_k=1)), 0)
        rows = self.rows()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["rank"], "1")

    def test_a_match_threshold_above_the_peak_count_reports_nothing(self) -> None:
        # Six matched peaks are impossible for a five-peak spectrum, so this
        # proves the filter is applied rather than merely accepted.
        self.assertEqual(library_search.run(self.args(min_matches=6)), 0)
        self.assertEqual(self.rows(), [])

    def test_the_pair_budget_stops_the_search_before_it_starts(self) -> None:
        with self.assertRaisesRegex(ValueError, "above --max-pairs"):
            library_search.run(self.args(max_pairs=2))
        # Nothing was written, so a refused run cannot look like an empty result.
        self.assertFalse(self.output.exists())

    def test_a_library_that_processing_empties_is_reported(self) -> None:
        # Requiring more peaks than any spectrum has leaves nothing to search.
        with self.assertRaisesRegex(ValueError, "no query spectra remain"):
            library_search.run(self.args(min_peaks=99))

    def test_main_turns_a_validation_error_into_exit_code_two(self) -> None:
        argv = [
            "library_search.py",
            str(self.root / "absent.mgf"),
            str(self.references),
            str(self.output),
        ]
        original = sys.argv
        sys.argv = argv
        try:
            self.assertEqual(library_search.main(), 2)
        finally:
            sys.argv = original


class VersionPinTests(unittest.TestCase):
    def test_the_installed_version_is_reported_rather_than_assumed(self) -> None:
        # `run` compares this against TARGET_VERSION to warn about drift, so it
        # must be a real version string and not the "unknown" fallback.
        reported = library_search.installed_matchms_version()
        self.assertRegex(reported, r"^\d+\.\d+")
        self.assertRegex(library_search.TARGET_VERSION, r"^\d+\.\d+\.\d+$")

    def test_the_documented_target_matches_the_skill_metadata(self) -> None:
        # SKILL.md tells the agent which release the script was verified on.
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(library_search.TARGET_VERSION, text)


if __name__ == "__main__":
    unittest.main()
