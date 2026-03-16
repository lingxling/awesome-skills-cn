import sys
import tempfile
import unittest
from pathlib import Path


TOOLS_SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_SCRIPTS_DIR))

import sync_microsoft_skills as sms


class SyncMicrosoftSkillsSecurityTests(unittest.TestCase):
    def test_sanitize_flat_name_rejects_path_traversal(self):
        sanitized = sms.sanitize_flat_name("../../.ssh", "fallback-name")
        self.assertEqual(sanitized, "fallback-name")

    def test_find_skills_ignores_symlinks_outside_clone(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skills_dir = root / "skills"
            skills_dir.mkdir()

            safe_skill = root / ".github" / "skills" / "safe-skill"
            safe_skill.mkdir(parents=True)
            (safe_skill / "SKILL.md").write_text("---\nname: safe-skill\n---\n", encoding="utf-8")
            (skills_dir / "safe-skill").symlink_to(safe_skill, target_is_directory=True)

            outside = Path(tempfile.mkdtemp())
            try:
                (outside / "SKILL.md").write_text("---\nname: leaked\n---\n", encoding="utf-8")
                (skills_dir / "escape").symlink_to(outside, target_is_directory=True)

                entries = sms.find_skills_in_directory(root)
                relative_paths = {str(entry["relative_path"]) for entry in entries}

                self.assertEqual(relative_paths, {"safe-skill"})
            finally:
                for child in outside.iterdir():
                    child.unlink()
                outside.rmdir()


if __name__ == "__main__":
    unittest.main()
