"""Tests for the literature-review result processing.

`search_databases` is pure list manipulation over records from several
databases, so it is fully testable offline -- and worth testing, because every
function here can lose papers silently. Deduplication that trusts a title
merges two distinct papers; a year filter that drops unparseable years quietly
shrinks the corpus; ranking that treats a missing citation count as zero
buries new work.

The schematic scripts this skill also ships are covered by the shared
contract, since `scientific-schematics` and `latex-posters` ship identical
copies.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import skill_contract

SKILL_ROOT = Path(__file__).resolve().parents[2] / "skills" / "literature-review"
SCRIPTS = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import search_databases  # noqa: E402

SchematicTests = skill_contract.schematic.schematic_test_case(SKILL_ROOT)
ReviewParsingTests = skill_contract.schematic.review_parsing_test_case(
    SCRIPTS, "generate_schematic_ai"
)
ReviewFailureTests = skill_contract.schematic.review_failure_test_case(
    SCRIPTS, "generate_schematic_ai", "ScientificSchematicGenerator",
    ("diagram.png", "a prompt", 1, "journal", 2),
)

RESULTS = [
    {
        "title": "Deep Learning for Protein Folding",
        "authors": "Jumper, J. and Evans, R.",
        "first_author": "Jumper",
        "year": "2021",
        "source": "PubMed",
        "doi": "10.1038/s41586-021-03819-2",
        "citations": 15000,
        "journal": "Nature",
    },
    {
        "title": "Attention Is All You Need",
        "authors": "Vaswani, A.",
        "first_author": "Vaswani",
        "year": "2017",
        "source": "arXiv",
        "citations": 90000,
    },
    {
        "title": "A Recent Preprint",
        "authors": "Smith, J.",
        "first_author": "Smith",
        "year": "2026",
        "source": "bioRxiv",
    },
]


class DeduplicationTests(unittest.TestCase):
    def test_records_sharing_a_doi_collapse_to_one(self) -> None:
        duplicated = [
            {"title": "One Version", "doi": "10.1000/x"},
            {"title": "Another Title Entirely", "doi": "10.1000/X"},
        ]
        self.assertEqual(len(search_databases.deduplicate_results(duplicated)), 1)

    def test_doi_comparison_ignores_case_and_surrounding_space(self) -> None:
        duplicated = [
            {"title": "a", "doi": " 10.1000/X "},
            {"title": "b", "doi": "10.1000/x"},
        ]
        self.assertEqual(len(search_databases.deduplicate_results(duplicated)), 1)

    def test_titles_only_deduplicate_records_that_have_no_doi(self) -> None:
        # Two records with the same title but different DOIs are two papers.
        distinct = [
            {"title": "Same Title", "doi": "10.1000/a"},
            {"title": "Same Title", "doi": "10.1000/b"},
        ]
        self.assertEqual(len(search_databases.deduplicate_results(distinct)), 2)

        same = [{"title": "Same Title"}, {"title": "same title"}]
        self.assertEqual(len(search_databases.deduplicate_results(same)), 1)

    def test_the_first_occurrence_is_the_one_kept(self) -> None:
        records = [
            {"title": "first", "doi": "10.1000/x", "source": "PubMed"},
            {"title": "second", "doi": "10.1000/x", "source": "arXiv"},
        ]
        self.assertEqual(
            search_databases.deduplicate_results(records)[0]["source"], "PubMed"
        )

    def test_an_empty_list_deduplicates_to_an_empty_list(self) -> None:
        self.assertEqual(search_databases.deduplicate_results([]), [])

    def test_records_with_neither_doi_nor_title_are_all_kept(self) -> None:
        records = [{"source": "a"}, {"source": "b"}]
        self.assertEqual(len(search_databases.deduplicate_results(records)), 2)


class RankingTests(unittest.TestCase):
    def test_citation_ranking_puts_the_most_cited_first(self) -> None:
        ranked = search_databases.rank_results(RESULTS, "citations")
        self.assertEqual(ranked[0]["title"], "Attention Is All You Need")
        self.assertEqual(ranked[-1]["title"], "A Recent Preprint")

    def test_year_ranking_puts_the_newest_first(self) -> None:
        ranked = search_databases.rank_results(RESULTS, "year")
        self.assertEqual(ranked[0]["year"], "2026")
        self.assertEqual(ranked[-1]["year"], "2017")

    def test_relevance_ranking_uses_the_relevance_score(self) -> None:
        scored = [
            {"title": "low", "relevance_score": 0.1},
            {"title": "high", "relevance_score": 0.9},
        ]
        self.assertEqual(
            search_databases.rank_results(scored, "relevance")[0]["title"], "high"
        )

    def test_an_unknown_criterion_leaves_the_order_untouched(self) -> None:
        self.assertEqual(
            [r["title"] for r in search_databases.rank_results(RESULTS, "nonsense")],
            [r["title"] for r in RESULTS],
        )

    def test_ranking_does_not_mutate_the_input(self) -> None:
        original = [dict(record) for record in RESULTS]
        search_databases.rank_results(RESULTS, "citations")
        self.assertEqual(RESULTS, original)

    def test_a_missing_citation_count_sorts_last_rather_than_erroring(self) -> None:
        ranked = search_databases.rank_results(RESULTS, "citations")
        self.assertNotIn("citations", ranked[-1])


class YearFilterTests(unittest.TestCase):
    def test_both_bounds_are_inclusive(self) -> None:
        filtered = search_databases.filter_by_year(RESULTS, 2017, 2021)
        self.assertEqual(len(filtered), 2)
        self.assertEqual({r["year"] for r in filtered}, {"2017", "2021"})

    def test_each_bound_can_be_used_alone(self) -> None:
        self.assertEqual(len(search_databases.filter_by_year(RESULTS, start_year=2021)), 2)
        self.assertEqual(len(search_databases.filter_by_year(RESULTS, end_year=2017)), 1)

    def test_no_bounds_keeps_everything(self) -> None:
        self.assertEqual(len(search_databases.filter_by_year(RESULTS)), len(RESULTS))

    def test_an_unparseable_year_is_kept_rather_than_silently_dropped(self) -> None:
        # Losing a paper because a database returned "in press" would be worse
        # than including one outside the range.
        records = [{"title": "x", "year": "in press"}, {"title": "y", "year": None}]
        self.assertEqual(len(search_databases.filter_by_year(records, 2020, 2026)), 2)

    def test_filtering_does_not_mutate_the_input(self) -> None:
        original = [dict(record) for record in RESULTS]
        search_databases.filter_by_year(RESULTS, 2020, 2022)
        self.assertEqual(RESULTS, original)


class SummaryTests(unittest.TestCase):
    def test_the_summary_counts_records_sources_and_years(self) -> None:
        summary = search_databases.generate_search_summary(RESULTS)
        self.assertEqual(summary["total_results"], 3)
        self.assertEqual(
            summary["sources"], {"PubMed": 1, "arXiv": 1, "bioRxiv": 1}
        )
        self.assertEqual(summary["year_distribution"]["2021"], 1)

    def test_citation_statistics_ignore_records_without_a_count(self) -> None:
        summary = search_databases.generate_search_summary(RESULTS)
        self.assertEqual(summary["total_citations"], 105000)
        self.assertEqual(summary["avg_citations"], 105000 / 2)

    def test_an_empty_corpus_summarises_to_zeroes_not_an_error(self) -> None:
        summary = search_databases.generate_search_summary([])
        self.assertEqual(summary["total_results"], 0)
        self.assertEqual(summary["avg_citations"], 0)
        self.assertEqual(summary["sources"], {})

    def test_a_non_numeric_citation_count_is_skipped(self) -> None:
        summary = search_databases.generate_search_summary(
            [{"citations": "many"}, {"citations": 10}]
        )
        self.assertEqual(summary["total_citations"], 10)

    def test_records_with_no_source_are_bucketed_as_unknown(self) -> None:
        summary = search_databases.generate_search_summary([{"title": "x"}])
        self.assertEqual(summary["sources"], {"Unknown": 1})


class FormattingTests(unittest.TestCase):
    def test_json_output_round_trips(self) -> None:
        rendered = search_databases.format_search_results(RESULTS, "json")
        self.assertEqual(json.loads(rendered), RESULTS)

    def test_markdown_lists_every_record_with_a_resolvable_doi_link(self) -> None:
        rendered = search_databases.format_search_results(RESULTS, "markdown")
        for record in RESULTS:
            with self.subTest(title=record["title"]):
                self.assertIn(record["title"], rendered)
        self.assertIn("https://doi.org/10.1038/s41586-021-03819-2", rendered)
        self.assertIn("**Total Results**: 3", rendered)

    def test_markdown_substitutes_placeholders_for_absent_fields(self) -> None:
        rendered = search_databases.format_search_results([{}], "markdown")
        self.assertIn("Untitled", rendered)
        self.assertIn("Unknown", rendered)
        self.assertIn("N/A", rendered)

    def test_bibtex_entries_are_balanced_and_keyed_by_author_and_year(self) -> None:
        rendered = search_databases.format_search_results(RESULTS, "bibtex")
        self.assertIn("@article{Jumper2021,", rendered)
        self.assertIn("journal = {Nature},", rendered)
        self.assertEqual(rendered.count("@"), 3)
        self.assertEqual(rendered.count("{"), rendered.count("}"))

    def test_bibtex_omits_fields_the_record_does_not_have(self) -> None:
        rendered = search_databases.format_search_results([RESULTS[1]], "bibtex")
        self.assertNotIn("journal =", rendered)
        self.assertNotIn("volume =", rendered)

    def test_bibtex_falls_back_to_a_placeholder_key(self) -> None:
        rendered = search_databases.format_search_results([{}], "bibtex")
        self.assertIn("@article{unknown0000,", rendered)

    def test_an_unknown_format_is_refused_by_name(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unknown format: ris"):
            search_databases.format_search_results(RESULTS, "ris")

    def test_an_empty_corpus_formats_without_error(self) -> None:
        for output_format in ("json", "markdown", "bibtex"):
            with self.subTest(output_format=output_format):
                rendered = search_databases.format_search_results([], output_format)
                self.assertIsInstance(rendered, str)


class PipelineTests(unittest.TestCase):
    def test_dedupe_filter_and_rank_compose_into_a_stable_corpus(self) -> None:
        raw = RESULTS + [dict(RESULTS[0])]  # the same paper found twice
        processed = search_databases.rank_results(
            search_databases.filter_by_year(
                search_databases.deduplicate_results(raw), 2017, 2026
            ),
            "citations",
        )
        titles = [record["title"] for record in processed]
        self.assertEqual(len(titles), 3)
        self.assertEqual(titles[0], "Attention Is All You Need")


class DependencyCheckTests(unittest.TestCase):
    def test_the_pdf_generator_reports_missing_tooling_rather_than_crashing(self) -> None:
        import generate_pdf

        # check_dependencies inspects the host for pandoc/LaTeX; whatever it
        # finds, it must answer rather than raise.
        result = generate_pdf.check_dependencies()
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
