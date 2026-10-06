"""Tests for the MarkItDown batch converters.

Conversion itself is MarkItDown's job. What these scripts own is everything
around it, and each piece has a failure mode worth guarding:

* `discover_files` decides what gets converted -- and must not silently pick up
  audio and video, because with `markitdown[all]` those are transcribed via
  Google Web Speech, sending local files off the machine.
* `output_path_for` preserves the source suffix in the output name, so
  `report.pdf` and `report.docx` do not collide on `report.md`.
* `atomic_write_text` replaces files through a temporary, so an interrupted
  run never leaves a half-written markdown file.
* `infer_metadata` reads `Author_Year_Title.pdf`, and a loose pattern would
  attribute papers to the wrong author.
"""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

import pytest

import skill_contract

SKILL_ROOT = Path(__file__).resolve().parents[2] / "skills" / "markitdown"
SCRIPTS = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

pytest.importorskip("markitdown", reason="markitdown scripts import markitdown")

import batch_convert  # noqa: E402
import convert_literature  # noqa: E402
import inspect_installation  # noqa: E402

CliHelpTests = skill_contract.cli.help_test_case(SKILL_ROOT)


class ExtensionTests(unittest.TestCase):
    def test_extensions_are_lowercased_dotted_and_deduplicated(self) -> None:
        self.assertEqual(
            batch_convert.normalize_extensions(["PDF", ".pdf", "docx", " .DOCX "]),
            (".docx", ".pdf"),
        )

    def test_blank_entries_are_dropped(self) -> None:
        self.assertEqual(batch_convert.normalize_extensions(["pdf", "", "   "]), (".pdf",))

    def test_an_empty_selection_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "At least one file extension"):
            batch_convert.normalize_extensions([])

    def test_a_lone_dot_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "cannot be only"):
            batch_convert.normalize_extensions(["."])

    def test_the_result_is_sorted_so_runs_are_reproducible(self) -> None:
        self.assertEqual(
            batch_convert.normalize_extensions(["xlsx", "csv", "pdf"]),
            (".csv", ".pdf", ".xlsx"),
        )

    def test_the_defaults_carry_no_audio_or_video_formats(self) -> None:
        # Converting those with markitdown[all] would ship the file to Google
        # Web Speech; they must be opt-in, never a default.
        overlap = set(batch_convert.DEFAULT_EXTENSIONS) & batch_convert.EXTERNAL_SERVICE_EXTENSIONS
        self.assertEqual(overlap, set())

    def test_the_defaults_are_sorted_lowercase_and_dotted(self) -> None:
        defaults = batch_convert.DEFAULT_EXTENSIONS
        self.assertEqual(list(defaults), sorted(defaults))
        for extension in defaults:
            with self.subTest(extension=extension):
                self.assertTrue(extension.startswith("."))
                self.assertEqual(extension, extension.lower())


class DiscoveryTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary.cleanup)
        self.root = Path(self._temporary.name)

    def touch(self, relative: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"x")
        return path


class DiscoveryTests(DiscoveryTestCase):
    def test_only_the_requested_extensions_are_returned(self) -> None:
        self.touch("a.pdf")
        self.touch("b.docx")
        self.touch("c.mp3")
        found = batch_convert.discover_files(self.root, (".pdf", ".docx"), recursive=False)
        self.assertEqual([path.name for path in found], ["a.pdf", "b.docx"])

    def test_matching_is_case_insensitive(self) -> None:
        self.touch("SCAN.PDF")
        found = batch_convert.discover_files(self.root, (".pdf",), recursive=False)
        self.assertEqual([path.name for path in found], ["SCAN.PDF"])

    def test_recursion_is_opt_in(self) -> None:
        self.touch("top.pdf")
        self.touch("nested/deep.pdf")

        shallow = batch_convert.discover_files(self.root, (".pdf",), recursive=False)
        self.assertEqual([path.name for path in shallow], ["top.pdf"])

        deep = batch_convert.discover_files(self.root, (".pdf",), recursive=True)
        self.assertEqual(sorted(path.name for path in deep), ["deep.pdf", "top.pdf"])

    def test_directories_are_never_returned(self) -> None:
        (self.root / "folder.pdf").mkdir()
        self.assertEqual(
            batch_convert.discover_files(self.root, (".pdf",), recursive=False), []
        )

    def test_the_order_is_deterministic(self) -> None:
        for name in ("c.pdf", "a.pdf", "b.pdf"):
            self.touch(name)
        found = batch_convert.discover_files(self.root, (".pdf",), recursive=False)
        self.assertEqual([path.name for path in found], ["a.pdf", "b.pdf", "c.pdf"])

    def test_an_empty_directory_yields_nothing(self) -> None:
        self.assertEqual(
            batch_convert.discover_files(self.root, (".pdf",), recursive=True), []
        )


class OutputPathTests(unittest.TestCase):
    def test_the_source_suffix_is_kept_in_the_output_name(self) -> None:
        # Without this, report.pdf and report.docx both become report.md and
        # the second silently overwrites the first.
        pdf = batch_convert.output_path_for(
            Path("/in/report.pdf"), Path("/in"), Path("/out")
        )
        docx = batch_convert.output_path_for(
            Path("/in/report.docx"), Path("/in"), Path("/out")
        )
        self.assertEqual(pdf, Path("/out/report.pdf.md"))
        self.assertEqual(docx, Path("/out/report.docx.md"))
        self.assertNotEqual(pdf, docx)

    def test_the_directory_layout_is_mirrored(self) -> None:
        self.assertEqual(
            batch_convert.output_path_for(
                Path("/in/2024/papers/a.pdf"), Path("/in"), Path("/out")
            ),
            Path("/out/2024/papers/a.pdf.md"),
        )


class AtomicWriteTests(DiscoveryTestCase):
    def test_the_content_lands_at_the_destination(self) -> None:
        path = self.root / "nested" / "out.md"
        batch_convert.atomic_write_text(path, "# Title\n")
        self.assertEqual(path.read_text(encoding="utf-8"), "# Title\n")

    def test_no_temporary_file_survives(self) -> None:
        path = self.root / "out.md"
        batch_convert.atomic_write_text(path, "content")
        self.assertEqual([entry.name for entry in self.root.iterdir()], ["out.md"])

    def test_an_existing_file_is_replaced_wholesale(self) -> None:
        path = self.root / "out.md"
        batch_convert.atomic_write_text(path, "a much longer original document")
        batch_convert.atomic_write_text(path, "short")
        self.assertEqual(path.read_text(encoding="utf-8"), "short")

    def test_non_ascii_content_survives_the_round_trip(self) -> None:
        path = self.root / "out.md"
        batch_convert.atomic_write_text(path, "Grüße — 日本語\n")
        self.assertEqual(path.read_text(encoding="utf-8"), "Grüße — 日本語\n")


class MetadataInferenceTests(unittest.TestCase):
    def test_an_author_year_title_filename_is_parsed(self) -> None:
        author, year, title = convert_literature.infer_metadata(
            Path("Jumper_2021_Highly_accurate_protein_structure.pdf")
        )
        self.assertEqual(author, "Jumper")
        self.assertEqual(year, "2021")
        self.assertEqual(title, "Highly accurate protein structure")

    def test_a_multi_word_author_is_kept_whole(self) -> None:
        author, year, _ = convert_literature.infer_metadata(
            Path("Van_Der_Berg_1998_A_study.pdf")
        )
        self.assertEqual(year, "1998")
        self.assertEqual(author, "Van Der Berg")

    def test_only_plausible_years_are_accepted(self) -> None:
        # 1899 and 2101 are not publication years the pattern should trust.
        for stem in ("Smith_1899_Old.pdf", "Smith_2101_Future.pdf", "Smith_21_Short.pdf"):
            with self.subTest(stem=stem):
                author, year, title = convert_literature.infer_metadata(Path(stem))
                self.assertIsNone(author)
                self.assertIsNone(year)
                self.assertTrue(title)

    def test_an_unstructured_filename_still_yields_a_readable_title(self) -> None:
        author, year, title = convert_literature.infer_metadata(
            Path("some_random_notes.pdf")
        )
        self.assertIsNone(author)
        self.assertIsNone(year)
        self.assertEqual(title, "some random notes")

    def test_runs_of_whitespace_are_collapsed(self) -> None:
        self.assertEqual(
            convert_literature.humanize_filename_component("a__b___c"), "a b c"
        )
        self.assertEqual(convert_literature.humanize_filename_component("  x  "), "x")


class DigestTests(DiscoveryTestCase):
    def test_the_digest_matches_hashlib(self) -> None:
        path = self.root / "paper.pdf"
        payload = b"%PDF-1.7\n" + b"x" * 5000
        path.write_bytes(payload)
        self.assertEqual(
            convert_literature.digest_file(path), hashlib.sha256(payload).hexdigest()
        )

    def test_an_empty_file_hashes_to_the_empty_digest(self) -> None:
        path = self.root / "empty.pdf"
        path.write_bytes(b"")
        self.assertEqual(
            convert_literature.digest_file(path), hashlib.sha256(b"").hexdigest()
        )

    def test_a_file_larger_than_one_chunk_is_hashed_whole(self) -> None:
        # The reader streams in 1 MiB chunks; a bug there would hash a prefix.
        path = self.root / "large.pdf"
        payload = bytes(range(256)) * 8192  # 2 MiB
        path.write_bytes(payload)
        self.assertEqual(
            convert_literature.digest_file(path), hashlib.sha256(payload).hexdigest()
        )


class YamlScalarTests(unittest.TestCase):
    def test_ordinary_text_is_quoted(self) -> None:
        self.assertEqual(convert_literature.yaml_scalar("A Title"), '"A Title"')

    def test_quotes_and_colons_are_escaped_safely(self) -> None:
        # An unquoted colon would end the YAML key and corrupt the front matter.
        rendered = convert_literature.yaml_scalar('He said: "hi"')
        self.assertEqual(json.loads(rendered), 'He said: "hi"')

    def test_non_ascii_is_preserved_rather_than_escaped(self) -> None:
        self.assertEqual(convert_literature.yaml_scalar("Grüße"), '"Grüße"')


class InstallationReportTests(unittest.TestCase):
    def test_the_report_names_the_target_version_and_optional_extras(self) -> None:
        self.assertRegex(inspect_installation.TARGET_VERSION, r"^\d+\.\d+\.\d+$")
        self.assertTrue(inspect_installation.OPTIONAL_DISTRIBUTIONS)

    def test_the_report_is_json_serialisable(self) -> None:
        json.dumps(inspect_installation.inspect_installation())

    def test_an_absent_distribution_reports_none_rather_than_raising(self) -> None:
        self.assertIsNone(
            inspect_installation.distribution_version("definitely-not-installed-xyz")
        )

    def test_an_installed_distribution_reports_its_version(self) -> None:
        self.assertIsNotNone(inspect_installation.distribution_version("markitdown"))


if __name__ == "__main__":
    unittest.main()
