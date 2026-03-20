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


audit_skills = load_module("tools/scripts/audit_skills.py", "audit_skills")


class AuditSkillsTests(unittest.TestCase):
    def test_audit_marks_complete_skill_as_ok(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skills_dir = root / "skills"
            skill_dir = skills_dir / "good-skill"
            skill_dir.mkdir(parents=True)

            (skill_dir / "SKILL.md").write_text(
                """---
name: good-skill
description: Useful and complete skill description
risk: safe
source: self
date_added: 2026-03-20
---

# Good Skill

## When to Use
- Use when the user needs a solid example.

## Examples
```bash
echo "hello"
```

## Limitations
- Demo only.
""",
                encoding="utf-8",
            )

            report = audit_skills.audit_skills(skills_dir)

            self.assertEqual(report["summary"]["skills_scanned"], 1)
            self.assertEqual(report["summary"]["skills_ok"], 1)
            self.assertEqual(report["summary"]["warnings"], 0)
            self.assertEqual(report["summary"]["errors"], 0)
            self.assertEqual(report["skills"][0]["status"], "ok")

    def test_audit_flags_truncated_description_and_missing_sections(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skills_dir = root / "skills"
            skill_dir = skills_dir / "truncated-skill"
            skill_dir.mkdir(parents=True)

            (skill_dir / "SKILL.md").write_text(
                """---
name: truncated-skill
description: This description was cut off...
risk: safe
source: self
---

# Truncated Skill

## When to Use
- Use when reproducing issue 365.
""",
                encoding="utf-8",
            )

            report = audit_skills.audit_skills(skills_dir)
            finding_codes = {finding["code"] for finding in report["skills"][0]["findings"]}

            self.assertEqual(report["skills"][0]["status"], "warning")
            self.assertIn("description_truncated", finding_codes)
            self.assertIn("missing_examples", finding_codes)
            self.assertIn("missing_limitations", finding_codes)

    def test_audit_flags_blocking_errors(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skills_dir = root / "skills"
            skill_dir = skills_dir / "offensive-skill"
            skill_dir.mkdir(parents=True)
            (skill_dir / "missing.md").write_text("# missing\n", encoding="utf-8")

            (skill_dir / "SKILL.md").write_text(
                """---
name: offensive-skill
description: Offensive example skill
risk: offensive
source: self
---

# Offensive Skill

## When to Use
- Use only in authorized environments.

## Examples
```bash
cat missing.md
```

See [details](missing-reference.md).

## Limitations
- Example only.
""",
                encoding="utf-8",
            )

            report = audit_skills.audit_skills(skills_dir)
            finding_codes = {finding["code"] for finding in report["skills"][0]["findings"]}

            self.assertEqual(report["skills"][0]["status"], "error")
            self.assertIn("dangling_link", finding_codes)
            self.assertIn("missing_authorized_use_only", finding_codes)


if __name__ == "__main__":
    unittest.main()
