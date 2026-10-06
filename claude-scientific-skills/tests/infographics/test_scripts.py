"""Tests for the infographics generator CLI.

Generation goes through OpenRouter, so nothing here calls it. What is testable
offline is the part that decides what the subprocess sees and what the user may
ask for: the environment allowlist (the same design as the schematic scripts --
forward a named set, never the whole parent environment) and the option
catalogue, where `--list-options` documents choices that argparse must actually
accept.

The palette presets get their own attention: this skill advertises them as
colourblind-safe, and a preset the generator does not know is a silent
downgrade to whatever it picks instead.
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

import skill_contract

SKILL_ROOT = Path(__file__).resolve().parents[2] / "skills" / "infographics"
SCRIPTS = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import generate_infographic  # noqa: E402

CliHelpTests = skill_contract.cli.help_test_case(SKILL_ROOT)

# `generate_infographic_ai.py` is a fork of the schematic generator and shares
# its review-parsing code, so it reuses the same contract.
ReviewParsingTests = skill_contract.schematic.review_parsing_test_case(
    SCRIPTS, "generate_infographic_ai"
)
ReviewFailureTests = skill_contract.schematic.review_failure_test_case(
    SCRIPTS, "generate_infographic_ai", "InfographicGenerator",
    ("infographic.png", "a prompt", "statistical", 1, "default", 3),
)


class SubprocessEnvironmentTests(unittest.TestCase):
    def test_only_allowlisted_variables_are_forwarded(self) -> None:
        environment = {
            "PATH": "/usr/bin",
            "HOME": "/home/someone",
            "AWS_SECRET_ACCESS_KEY": "must-not-leak",
            "SLACK_TOKEN": "also-not",
        }
        with mock.patch.dict("os.environ", environment, clear=True):
            built = generate_infographic.build_subprocess_env(None)
        self.assertEqual(set(built), {"PATH", "HOME"})

    def test_the_api_key_is_injected_when_supplied(self) -> None:
        with mock.patch.dict("os.environ", {"PATH": "/usr/bin"}, clear=True):
            built = generate_infographic.build_subprocess_env("sk-or-test")
        self.assertEqual(built["OPENROUTER_API_KEY"], "sk-or-test")

    def test_an_empty_key_is_omitted_rather_than_passed_blank(self) -> None:
        with mock.patch.dict("os.environ", {"PATH": "/usr/bin"}, clear=True):
            for value in (None, ""):
                with self.subTest(value=value):
                    self.assertNotIn(
                        "OPENROUTER_API_KEY",
                        generate_infographic.build_subprocess_env(value),
                    )

    def test_the_allowlist_carries_no_credential_variables(self) -> None:
        forwarded = " ".join(generate_infographic.FORWARDED_ENV_VARS).upper()
        for banned in ("SECRET", "TOKEN", "PASSWORD", "API_KEY", "CREDENTIAL"):
            with self.subTest(term=banned):
                self.assertNotIn(banned, forwarded)

    def test_the_allowlist_keeps_tls_and_proxy_settings_working(self) -> None:
        forwarded = set(generate_infographic.FORWARDED_ENV_VARS)
        for required in ("HTTPS_PROXY", "https_proxy", "SSL_CERT_FILE", "REQUESTS_CA_BUNDLE"):
            with self.subTest(variable=required):
                self.assertIn(required, forwarded)

    def test_the_allowlist_matches_the_schematic_scripts(self) -> None:
        # Both CLIs solve the same problem the same way; a divergence means one
        # of them was updated and the other forgotten.
        schematic = (
            SKILL_ROOT.parent / "scientific-schematics" / "scripts" / "generate_schematic.py"
        ).read_text(encoding="utf-8")
        for variable in generate_infographic.FORWARDED_ENV_VARS:
            with self.subTest(variable=variable):
                self.assertIn(f'"{variable}"', schematic)


class OptionCatalogueTests(unittest.TestCase):
    CATALOGUES = {
        "type": "INFOGRAPHIC_TYPES",
        "style": "STYLE_PRESETS",
        "palette": "PALETTE_PRESETS",
        "doc-type": "DOC_TYPES",
    }

    def setUp(self) -> None:
        self.source = (SCRIPTS / "generate_infographic.py").read_text(encoding="utf-8")

    def test_every_catalogue_is_non_empty_and_free_of_duplicates(self) -> None:
        for attribute in self.CATALOGUES.values():
            with self.subTest(catalogue=attribute):
                values = getattr(generate_infographic, attribute)
                self.assertTrue(values)
                self.assertEqual(len(set(values)), len(values))

    def test_every_catalogued_value_is_documented_by_list_options(self) -> None:
        import io
        from contextlib import redirect_stdout

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            generate_infographic.list_options()
        documented = buffer.getvalue()

        for attribute in self.CATALOGUES.values():
            for value in getattr(generate_infographic, attribute):
                with self.subTest(option=value):
                    self.assertIn(value, documented)

    def test_the_parser_offers_each_catalogue_as_choices(self) -> None:
        # `choices=` wired to the catalogue means adding an option is one edit;
        # a hand-copied list drifts.
        for flag, attribute in self.CATALOGUES.items():
            with self.subTest(flag=flag):
                self.assertIn(f"choices={attribute}", self.source)

    def test_the_palettes_are_the_recognised_colourblind_safe_sets(self) -> None:
        self.assertEqual(
            set(generate_infographic.PALETTE_PRESETS), {"wong", "ibm", "tol"}
        )

    def test_option_names_are_lowercase_slugs(self) -> None:
        for attribute in self.CATALOGUES.values():
            for value in getattr(generate_infographic, attribute):
                with self.subTest(option=value):
                    self.assertRegex(value, r"^[a-z][a-z0-9-]*$")


class ParserTests(unittest.TestCase):
    def test_help_lists_every_documented_flag(self) -> None:
        result = skill_contract.cli.run_help(SCRIPTS / "generate_infographic.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        for flag in ("--type", "--style", "--palette", "--doc-type", "--output"):
            with self.subTest(flag=flag):
                self.assertIn(flag, result.stdout)

    def test_an_unknown_option_value_is_rejected_at_the_boundary(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "generate_infographic.py"),
                "a prompt",
                "-o", "out.png",
                "--palette", "rainbow",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("rainbow", result.stderr)

    def test_the_generator_script_is_shipped(self) -> None:
        self.assertTrue((SCRIPTS / "generate_infographic_ai.py").is_file())


if __name__ == "__main__":
    unittest.main()
