"""Tests for the scientific-schematics generator.

The environment-allowlist and CLI behaviour live in the shared contract, since
`latex-posters` and `literature-review` ship byte-identical copies of both
scripts. What is specific to this skill is its bundled `example_usage.sh` and
the document-type quality thresholds the CLI advertises.
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

import skill_contract

SKILL_ROOT = Path(__file__).resolve().parents[2] / "skills" / "scientific-schematics"
SCRIPTS = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

SchematicTests = skill_contract.schematic.schematic_test_case(SKILL_ROOT)
ReviewParsingTests = skill_contract.schematic.review_parsing_test_case(
    SCRIPTS, "generate_schematic_ai"
)
ReviewFailureTests = skill_contract.schematic.review_failure_test_case(
    SCRIPTS, "generate_schematic_ai", "ScientificSchematicGenerator",
    ("diagram.png", "a prompt", 1, "journal", 2),
)
CliHelpTests = skill_contract.cli.help_test_case(SKILL_ROOT)


class DocumentTypeTests(unittest.TestCase):
    def test_every_advertised_document_type_is_an_accepted_choice(self) -> None:
        # The help epilogue lists thresholds per document type; a type named
        # there but absent from `choices` fails only at the user's keyboard.
        result = skill_contract.cli.run_help(SCRIPTS / "generate_schematic.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        help_text = result.stdout

        source = (SCRIPTS / "generate_schematic.py").read_text(encoding="utf-8")
        for document_type in (
            "journal", "conference", "poster", "presentation",
            "thesis", "grant", "preprint", "report", "default",
        ):
            with self.subTest(document_type=document_type):
                self.assertIn(document_type, help_text)
                self.assertIn(f'"{document_type}"', source)

    def test_the_output_flag_is_required(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "generate_schematic.py"), "a diagram"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--output", result.stderr)


class ExampleScriptTests(unittest.TestCase):
    def test_the_bundled_example_is_executable_shell(self) -> None:
        example = SCRIPTS / "example_usage.sh"
        self.assertTrue(example.is_file())
        self.assertTrue(example.stat().st_mode & 0o111, "not executable")
        self.assertTrue(
            example.read_text(encoding="utf-8").startswith("#!"), "no shebang"
        )
        syntax = subprocess.run(
            ["bash", "-n", str(example)], capture_output=True, text=True, timeout=30
        )
        self.assertEqual(syntax.returncode, 0, syntax.stderr)

    def test_the_example_only_invokes_scripts_the_skill_ships(self) -> None:
        text = (SCRIPTS / "example_usage.sh").read_text(encoding="utf-8")
        for token in text.split():
            if token.endswith(".py"):
                with self.subTest(script=token):
                    name = Path(token).name
                    self.assertTrue((SCRIPTS / name).is_file(), f"{name} is not shipped")


if __name__ == "__main__":
    unittest.main()
