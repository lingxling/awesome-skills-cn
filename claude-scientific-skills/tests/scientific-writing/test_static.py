"""Static safety and packaging tests for scientific-writing."""

from __future__ import annotations

import ast
import csv
import io
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "skills" / "scientific-writing"
REPO_ROOT = ROOT.parents[1]
SCRIPT_DIR = ROOT / "scripts"


class StaticTests(unittest.TestCase):
    def test_skill_frontmatter_and_length(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertLess(len(text.splitlines()), 500)
        self.assertTrue(text.startswith("---\n"))
        self.assertRegex(text, r'\n  version: "\d+\.\d+"\n')
        self.assertIn("license: MIT", text)
        self.assertIn("compatibility:", text)
        self.assertNotIn("required_environment_variables", text)
        self.assertNotIn("OPENROUTER_API_KEY", text)

    def test_removed_external_generation_files_stay_removed(self) -> None:
        removed = {
            "generate_image.py",
            "generate_schematic.py",
            "generate_schematic_ai.py",
            "scientific_report.sty",
            "scientific_report_template.tex",
        }
        present = {path.name for path in ROOT.rglob("*") if path.is_file()}
        self.assertTrue(removed.isdisjoint(present))

    def test_all_python_is_parseable(self) -> None:
        for path in sorted(ROOT.rglob("*.py")):
            with self.subTest(path=path.relative_to(ROOT)):
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    def test_runtime_scripts_have_no_network_dynamic_eval_or_process_imports(
        self,
    ) -> None:
        banned_import_roots = {
            "aiohttp",
            "dotenv",
            "httpx",
            "marshal",
            "pickle",
            "requests",
            "socket",
            "subprocess",
            "urllib",
        }
        banned_calls = {"eval", "exec", "compile", "__import__"}
        for path in sorted(SCRIPT_DIR.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            imported: set[str] = set()
            called: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported.update(alias.name.split(".")[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported.add(node.module.split(".")[0])
                elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    called.add(node.func.id)
            with self.subTest(path=path.name):
                self.assertTrue(banned_import_roots.isdisjoint(imported))
                self.assertTrue(banned_calls.isdisjoint(called))

    def test_runtime_scripts_do_not_read_environment(self) -> None:
        forbidden = (
            "os.environ",
            "os.getenv",
            "getenv(",
            "environ[",
            "load_dotenv",
        )
        for path in sorted(SCRIPT_DIR.glob("*.py")):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                for token in forbidden:
                    self.assertNotIn(token, text)

    def test_json_and_csv_assets_are_well_formed(self) -> None:
        for path in sorted((ROOT / "assets").glob("*.json")):
            with self.subTest(path=path.name):
                json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "assets").glob("*.csv")):
            with self.subTest(path=path.name):
                rows = list(csv.reader(io.StringIO(path.read_text(encoding="utf-8"))))
                self.assertGreaterEqual(len(rows), 2)
                self.assertEqual(len(rows[0]), len(rows[1]))

    def test_templates_are_explicitly_incomplete(self) -> None:
        manifest = json.loads(
            (ROOT / "assets" / "manuscript_manifest_template.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertFalse(manifest["submission_ready"])
        scaffold = (ROOT / "assets" / "manuscript_scaffold.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("NOT FOR SUBMISSION", scaffold)
        self.assertIn("[[TODO:", scaffold)

    def test_registry_sources_exist_in_dated_ledger(self) -> None:
        registry = json.loads(
            (ROOT / "assets" / "reporting_guidelines.json").read_text(encoding="utf-8")
        )
        ledger = (ROOT / "references" / "source_ledger.md").read_text(encoding="utf-8")
        self.assertIn("2026-07-24", ledger)
        ledger_ids = set(re.findall(r"SW-S[0-9]{2}", ledger))
        used_ids = {
            source_id
            for guideline in registry["guidelines"]
            for source_id in guideline["source_ids"]
        }
        self.assertTrue(used_ids.issubset(ledger_ids))

    def test_relative_markdown_links_resolve(self) -> None:
        link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        for path in sorted(ROOT.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            for target in link_re.findall(text):
                if (
                    target.startswith(("http://", "https://", "#", "mailto:"))
                    or " " in target
                ):
                    continue
                clean_target = target.split("#", 1)[0]
                if not clean_target:
                    continue
                with self.subTest(path=path.relative_to(ROOT), target=target):
                    self.assertTrue((path.parent / clean_target).resolve().is_file())

    def test_no_cross_skill_calls_or_external_image_workflows(self) -> None:
        text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(ROOT.rglob("*"))
            if (
                path.is_file()
                and path.suffix in {".md", ".py", ".json", ".csv"}
                and "tests" not in path.relative_to(ROOT).parts
            )
        )
        forbidden = {
            "research-lookup skill",
            "scientific-schematics",
            "venue-templates skill",
            "openrouter.ai",
            "generate_image.py",
            "generate_schematic.py",
        }
        self.assertTrue(all(token not in text for token in forbidden))

    def test_no_bytecode_or_cache_artifacts(self) -> None:
        artifacts = [
            path
            for path in ROOT.rglob("*")
            if path.is_file() and path.suffix in {".pyc", ".pyo"}
        ]
        self.assertEqual(artifacts, [])

    def test_changes_remain_scoped_to_skill(self) -> None:
        self.assertEqual(ROOT, REPO_ROOT / "skills" / "scientific-writing")


if __name__ == "__main__":
    unittest.main()
