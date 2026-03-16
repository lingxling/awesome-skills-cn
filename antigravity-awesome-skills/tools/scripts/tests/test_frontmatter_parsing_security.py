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
    spec.loader.exec_module(module)
    return module


generate_index = load_module("tools/scripts/generate_index.py", "generate_index")
validate_skills = load_module("tools/scripts/validate_skills.py", "validate_skills")


class FrontmatterParsingSecurityTests(unittest.TestCase):
    def test_generate_index_frontmatter_rejects_non_mapping(self):
        content = "---\njust-a-string\n---\nbody\n"
        metadata = generate_index.parse_frontmatter(content)

        self.assertEqual(metadata, {})

    def test_validate_skills_frontmatter_rejects_non_mapping(self):
        content = "---\njust-a-string\n---\nbody\n"
        metadata, errors = validate_skills.parse_frontmatter(content)

        self.assertIsNone(metadata)
        self.assertTrue(any("mapping" in error.lower() for error in errors))

    def test_validate_skills_normalizes_unquoted_yaml_dates(self):
        content = "---\nname: demo\ndescription: ok\ndate_added: 2026-03-15\n---\nbody\n"
        metadata, errors = validate_skills.parse_frontmatter(content)

        self.assertEqual(errors, [])
        self.assertEqual(metadata["date_added"], "2026-03-15")

    def test_generate_index_serializes_unquoted_yaml_dates(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skills_dir = root / "skills"
            skill_dir = skills_dir / "demo"
            output_file = root / "skills_index.json"

            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\nname: demo\ndescription: ok\ndate_added: 2026-03-15\n---\nBody\n",
                encoding="utf-8",
            )

            skills = generate_index.generate_index(str(skills_dir), str(output_file))

            self.assertEqual(skills[0]["date_added"], "2026-03-15")
            self.assertIn('"date_added": "2026-03-15"', output_file.read_text(encoding="utf-8"))

    def test_generate_index_ignores_symlinked_skill_markdown(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skills_dir = root / "skills"
            safe_skill = skills_dir / "safe-skill"
            linked_skill = skills_dir / "linked-skill"
            outside_dir = root / "outside"
            output_file = root / "skills_index.json"

            safe_skill.mkdir(parents=True)
            linked_skill.mkdir(parents=True)
            outside_dir.mkdir()

            (safe_skill / "SKILL.md").write_text("---\nname: safe-skill\ndescription: safe\n---\n", encoding="utf-8")
            target = outside_dir / "SKILL.md"
            target.write_text("---\nname: outside\ndescription: outside\n---\n", encoding="utf-8")
            (linked_skill / "SKILL.md").symlink_to(target)

            skills = generate_index.generate_index(str(skills_dir), str(output_file))

            self.assertEqual([skill["id"] for skill in skills], ["safe-skill"])


if __name__ == "__main__":
    unittest.main()
