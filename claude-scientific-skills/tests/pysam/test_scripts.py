"""Tests for the pysam alignment helpers.

Reading a BAM needs pysam, but the decisions these scripts make before opening
one do not: the file-mode chosen from the suffix (`rb` vs `rc` vs `r` -- get it
wrong and htslib misreads the file), the argument validators, and the
destination checks that stop a filter run from overwriting its own input.

Where a real alignment is needed the tests build one with pysam and skip when
it is unavailable, so the suite is meaningful in the project environment and
complete under `--isolated`.
"""

from __future__ import annotations

import argparse
import sys
import tempfile
import unittest
from pathlib import Path

import pytest

import skill_contract

SKILL_ROOT = Path(__file__).resolve().parents[2] / "skills" / "pysam"
SCRIPTS = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

pysam = pytest.importorskip("pysam", reason="pysam skill needs pysam")

import alignment_qc  # noqa: E402
import filter_alignments  # noqa: E402
import inspect_hts  # noqa: E402

CliHelpTests = skill_contract.cli.help_test_case(SKILL_ROOT)


class ArgumentValidatorTests(unittest.TestCase):
    def test_positive_int_accepts_only_values_above_zero(self) -> None:
        self.assertEqual(alignment_qc.positive_int("5"), 5)
        for value in ("0", "-1"):
            with self.subTest(value=value):
                with self.assertRaises(argparse.ArgumentTypeError):
                    alignment_qc.positive_int(value)

    def test_nonnegative_int_admits_zero(self) -> None:
        self.assertEqual(alignment_qc.nonnegative_int("0"), 0)
        with self.assertRaises(argparse.ArgumentTypeError):
            alignment_qc.nonnegative_int("-1")

    def test_non_numeric_input_raises(self) -> None:
        for validator in (alignment_qc.positive_int, alignment_qc.nonnegative_int):
            with self.subTest(validator=validator.__name__):
                with self.assertRaises(ValueError):
                    validator("many")

    def test_the_validators_are_shared_across_the_scripts(self) -> None:
        # Three scripts define the same pair; they must agree.
        for module in (alignment_qc, filter_alignments, inspect_hts):
            with self.subTest(module=module.__name__):
                self.assertEqual(module.positive_int("3"), 3)
                self.assertEqual(module.nonnegative_int("0"), 0)


class FileModeTests(unittest.TestCase):
    def test_the_htslib_mode_follows_the_suffix(self) -> None:
        cases = {"reads.sam": "r", "reads.bam": "rb", "reads.cram": "rc"}
        for name, expected in cases.items():
            with self.subTest(name=name):
                self.assertEqual(alignment_qc.alignment_mode(Path(name)), expected)

    def test_the_suffix_check_is_case_insensitive(self) -> None:
        self.assertEqual(alignment_qc.alignment_mode(Path("READS.BAM")), "rb")

    def test_an_unrecognised_suffix_is_refused(self) -> None:
        for name in ("reads.txt", "reads", "reads.bam.gz"):
            with self.subTest(name=name):
                with self.assertRaisesRegex(ValueError, r"\.sam, \.bam, or \.cram"):
                    alignment_qc.alignment_mode(Path(name))

    def test_the_writing_mode_differs_from_the_reading_mode(self) -> None:
        # htslib needs "wb" to write a BAM; reusing "rb" silently produces SAM.
        self.assertEqual(
            filter_alignments.alignment_mode(Path("out.bam"), writing=True), "wb"
        )
        self.assertEqual(
            filter_alignments.alignment_mode(Path("out.bam"), writing=False), "rb"
        )


class RatioTests(unittest.TestCase):
    def test_a_ratio_over_zero_is_none_rather_than_an_error(self) -> None:
        # An empty BAM must report "no reads", not divide by zero.
        self.assertIsNone(alignment_qc.ratio(0, 0))
        self.assertIsNone(alignment_qc.average(0, 0))

    def test_ordinary_ratios_and_averages(self) -> None:
        self.assertEqual(alignment_qc.ratio(1, 4), 0.25)
        self.assertEqual(alignment_qc.average(10, 4), 2.5)

    def test_a_zero_numerator_is_zero_not_none(self) -> None:
        self.assertEqual(alignment_qc.ratio(0, 10), 0.0)


class LocalFileTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary.cleanup)
        self.root = Path(self._temporary.name)

    def test_an_existing_file_is_returned(self) -> None:
        path = self.root / "reads.bam"
        path.write_bytes(b"")
        self.assertEqual(alignment_qc.require_local_file(path, "input"), path)

    def test_a_missing_path_is_reported_with_its_label(self) -> None:
        with self.assertRaisesRegex(FileNotFoundError, "input does not exist"):
            alignment_qc.require_local_file(self.root / "absent.bam", "input")

    def test_a_directory_is_not_a_regular_file(self) -> None:
        with self.assertRaisesRegex(ValueError, "not a regular file"):
            alignment_qc.require_local_file(self.root, "input")


class DestinationTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary.cleanup)
        self.root = Path(self._temporary.name)
        self.source = self.root / "in.bam"
        self.source.write_bytes(b"")

    def test_a_fresh_destination_is_accepted(self) -> None:
        filter_alignments.validate_destinations(
            self.source, self.root / "out.bam", None
        )

    def test_an_existing_output_is_never_overwritten(self) -> None:
        output = self.root / "out.bam"
        output.write_bytes(b"")
        with self.assertRaises(FileExistsError):
            filter_alignments.validate_destinations(self.source, output, None)

    def test_writing_over_the_input_is_refused(self) -> None:
        # Truncating the input mid-filter would destroy the only copy. The
        # exists-check happens to fire first, so accept either refusal --
        # what matters is that the call does not go through.
        with self.assertRaises((FileExistsError, ValueError)):
            filter_alignments.validate_destinations(self.source, self.source, None)

    def test_a_differently_spelled_path_to_the_input_is_also_refused(self) -> None:
        alias = self.root / "sub" / ".." / "in.bam"
        (self.root / "sub").mkdir()
        with self.assertRaises((FileExistsError, ValueError)):
            filter_alignments.validate_destinations(self.source, alias, None)

    def test_a_missing_output_directory_is_refused(self) -> None:
        with self.assertRaises(FileNotFoundError):
            filter_alignments.validate_destinations(
                self.source, self.root / "nope" / "out.bam", None
            )


class ExclusionTests(unittest.TestCase):
    """`exclusion_reasons` decides which reads a filter run drops, and why."""

    @staticmethod
    def flags(**overrides) -> argparse.Namespace:
        defaults = dict(
            exclude_unmapped=False,
            exclude_secondary=False,
            exclude_supplementary=False,
            exclude_duplicates=False,
            exclude_qcfail=False,
            proper_pairs_only=False,
            min_mapq=0,
        )
        defaults.update(overrides)
        return argparse.Namespace(**defaults)

    @staticmethod
    def read(**attributes):
        class Read:
            is_unmapped = False
            is_secondary = False
            is_supplementary = False
            is_duplicate = False
            is_qcfail = False
            is_proper_pair = True
            mapping_quality = 60

        read = Read()
        for name, value in attributes.items():
            setattr(read, name, value)
        return read

    def test_a_clean_read_has_no_exclusion_reasons(self) -> None:
        self.assertEqual(
            filter_alignments.exclusion_reasons(self.read(), self.flags()), []
        )

    def test_each_flag_excludes_only_its_own_category(self) -> None:
        cases = [
            ("exclude_unmapped", "is_unmapped", "unmapped"),
            ("exclude_secondary", "is_secondary", "secondary"),
            ("exclude_supplementary", "is_supplementary", "supplementary"),
            ("exclude_duplicates", "is_duplicate", "duplicate"),
            ("exclude_qcfail", "is_qcfail", "qc_fail"),
        ]
        for flag, attribute, reason in cases:
            with self.subTest(flag=flag):
                read = self.read(**{attribute: True})
                # Flag off: the read survives.
                self.assertEqual(
                    filter_alignments.exclusion_reasons(read, self.flags()), []
                )
                # Flag on: it is dropped with the documented reason.
                self.assertEqual(
                    filter_alignments.exclusion_reasons(read, self.flags(**{flag: True})),
                    [reason],
                )

    def test_a_read_below_the_mapq_threshold_is_dropped(self) -> None:
        read = self.read(mapping_quality=20)
        self.assertEqual(
            filter_alignments.exclusion_reasons(read, self.flags(min_mapq=30)),
            ["mapq_below_threshold"],
        )
        # The threshold is inclusive at the boundary.
        self.assertEqual(
            filter_alignments.exclusion_reasons(read, self.flags(min_mapq=20)), []
        )

    def test_improper_pairs_are_dropped_only_when_asked(self) -> None:
        read = self.read(is_proper_pair=False)
        self.assertEqual(filter_alignments.exclusion_reasons(read, self.flags()), [])
        self.assertEqual(
            filter_alignments.exclusion_reasons(
                read, self.flags(proper_pairs_only=True)
            ),
            ["not_proper_pair"],
        )

    def test_every_applicable_reason_is_reported_not_just_the_first(self) -> None:
        read = self.read(is_unmapped=True, is_duplicate=True, mapping_quality=0)
        reasons = filter_alignments.exclusion_reasons(
            read,
            self.flags(exclude_unmapped=True, exclude_duplicates=True, min_mapq=30),
        )
        self.assertEqual(
            set(reasons), {"unmapped", "duplicate", "mapq_below_threshold"}
        )


class KindDetectionTests(unittest.TestCase):
    def test_the_documented_kinds_are_the_advertised_set(self) -> None:
        self.assertEqual(
            set(inspect_hts.KINDS),
            {"alignment", "variant", "fasta", "fastx", "tabix"},
        )

    def test_alignment_suffixes_are_detected(self) -> None:
        for name in ("reads.bam", "reads.sam", "reads.cram"):
            with self.subTest(name=name):
                self.assertEqual(inspect_hts.detect_kind(Path(name)), "alignment")

    def test_variant_suffixes_are_detected(self) -> None:
        for name in ("calls.vcf", "calls.vcf.gz", "calls.bcf"):
            with self.subTest(name=name):
                self.assertEqual(inspect_hts.detect_kind(Path(name)), "variant")

    def test_detection_is_case_insensitive(self) -> None:
        self.assertEqual(inspect_hts.detect_kind(Path("READS.BAM")), "alignment")

    def test_every_detected_kind_is_one_the_script_handles(self) -> None:
        for name in ("a.bam", "a.vcf", "a.fa", "a.fastq", "a.bed.gz"):
            with self.subTest(name=name):
                try:
                    kind = inspect_hts.detect_kind(Path(name))
                except ValueError:
                    continue
                self.assertIn(kind, inspect_hts.KINDS)


if __name__ == "__main__":
    unittest.main()
