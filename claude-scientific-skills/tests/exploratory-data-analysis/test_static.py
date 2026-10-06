#!/usr/bin/env python3
"""Static and dependency-free CLI checks for exploratory-data-analysis."""

from __future__ import annotations

import ast
import os
import subprocess
import sys
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[2] / "skills" / "exploratory-data-analysis"
SCRIPTS = SKILL_ROOT / "scripts"
REFERENCES = SKILL_ROOT / "references"
PUBLIC_CLIS = (
    "capability_manifest.py",
    "distribution_sensitivity.py",
    "eda_analyzer.py",
    "image_inspector.py",
    "missingness_leakage_audit.py",
    "report_scaffold.py",
    "sequence_inspector.py",
    "tabular_profile.py",
)


def run_help(name: str) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, "-S", str(SCRIPTS / name), "--help"],
        cwd=SKILL_ROOT,
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )


class StaticSafetyTests(unittest.TestCase):
    def test_all_scripts_parse_and_avoid_dynamic_or_network_execution(self) -> None:
        banned_imports = {
            "aiohttp",
            "dill",
            "httpx",
            "joblib",
            "pickle",
            "requests",
            "socket",
            "subprocess",
            "urllib",
        }
        banned_calls = {"eval", "exec", "compile", "__import__"}
        for path in sorted(SCRIPTS.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    roots = {alias.name.split(".", 1)[0] for alias in node.names}
                    self.assertFalse(roots & banned_imports, path.name)
                if isinstance(node, ast.ImportFrom) and node.module:
                    self.assertNotIn(
                        node.module.split(".", 1)[0],
                        banned_imports,
                        path.name,
                    )
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    self.assertNotIn(node.func.id, banned_calls, path.name)
                if isinstance(node, ast.keyword) and node.arg == "allow_pickle":
                    self.assertFalse(
                        isinstance(node.value, ast.Constant)
                        and node.value.value is True,
                        path.name,
                    )

    def test_all_public_help_is_dependency_free(self) -> None:
        for name in PUBLIC_CLIS:
            with self.subTest(script=name):
                result = run_help(name)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("usage:", result.stdout.casefold())
                self.assertNotIn("Traceback", result.stderr)

    def test_frontmatter_version_and_progressive_disclosure(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("license: MIT", skill)
        self.assertIn("compatibility:", skill)
        self.assertRegex(skill, r'\nmetadata:\n  version: "\d+\.\d+"\n')
        self.assertNotIn("200+", skill)
        self.assertLess(len(skill.splitlines()), 500)

    def test_six_references_and_report_asset_are_present(self) -> None:
        self.assertEqual(
            {path.name for path in REFERENCES.glob("*.md")},
            {
                "bioinformatics_genomics_formats.md",
                "chemistry_molecular_formats.md",
                "general_scientific_formats.md",
                "microscopy_imaging_formats.md",
                "proteomics_metabolomics_formats.md",
                "spectroscopy_analytical_formats.md",
            },
        )
        template = (SKILL_ROOT / "assets" / "report_template.md").read_text(
            encoding="utf-8"
        )
        for required in (
            "Data dictionary",
            "Train, validation, and test boundaries",
            "Missingness, censoring, and detection limits",
            "Exploratory comparisons and multiplicity",
            "Reproducibility and provenance",
        ):
            self.assertIn(required, template)

if __name__ == "__main__":
    unittest.main()
