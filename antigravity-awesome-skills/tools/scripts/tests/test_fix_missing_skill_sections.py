import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLS_SCRIPTS_DIR = REPO_ROOT / "tools" / "scripts"
if str(TOOLS_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_SCRIPTS_DIR))


def load_module(relative_path: str, module_name: str):
    module_path = REPO_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


fix_missing_skill_sections = load_module(
    "tools/scripts/fix_missing_skill_sections.py",
    "fix_missing_skill_sections",
)


class FixMissingSkillSectionsTests(unittest.TestCase):
    def test_normalizes_when_heading_variant(self):
        content = """---
name: demo
description: Demo description.
---

# Demo

## When to Activate
Activate this skill when:
- something happens
"""
        updated = fix_missing_skill_sections.normalize_when_heading_variants(content)
        self.assertIn("## When to Use", updated)
        self.assertNotIn("## When to Activate", updated)

    def test_update_skill_file_adds_missing_sections(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_path = Path(temp_dir) / "SKILL.md"
            skill_path.write_text(
                """---
name: demo
description: Structured guide for setting up A/B tests with mandatory gates for hypothesis and metrics.
---

# Demo

Intro paragraph.
""",
                encoding="utf-8",
            )

            changed, changes = fix_missing_skill_sections.update_skill_file(skill_path, add_missing=True)
            updated = skill_path.read_text(encoding="utf-8")

            self.assertTrue(changed)
            self.assertIn("added_when_to_use", changes)
            self.assertIn("added_examples", changes)
            self.assertIn("## When to Use", updated)
            self.assertIn("## Examples", updated)
            self.assertIn("Use @demo for this task:", updated)

    def test_update_skill_file_only_adds_examples_when_when_section_exists(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_path = Path(temp_dir) / "SKILL.md"
            skill_path.write_text(
                """---
name: demo
description: Build and distribute Expo development clients locally or via TestFlight.
---

# Demo

## When to Use
- Use this skill when native Expo changes need a dev client.
""",
                encoding="utf-8",
            )

            changed, changes = fix_missing_skill_sections.update_skill_file(skill_path, add_missing=True)
            updated = skill_path.read_text(encoding="utf-8")

            self.assertTrue(changed)
            self.assertNotIn("added_when_to_use", changes)
            self.assertIn("added_examples", changes)
            self.assertEqual(updated.count("## When to Use"), 1)
            self.assertIn("## Examples", updated)

    def test_update_skill_file_defaults_to_normalization_only(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_path = Path(temp_dir) / "SKILL.md"
            skill_path.write_text(
                """---
name: demo
description: Demo description.
---

# Demo

## When to Activate
Activate this skill when:
- something happens
""",
                encoding="utf-8",
            )

            changed, changes = fix_missing_skill_sections.update_skill_file(skill_path)
            updated = skill_path.read_text(encoding="utf-8")

            self.assertTrue(changed)
            self.assertEqual(changes, ["normalized_when_heading"])
            self.assertIn("## When to Use", updated)
            self.assertNotIn("## Examples", updated)


if __name__ == "__main__":
    unittest.main()
