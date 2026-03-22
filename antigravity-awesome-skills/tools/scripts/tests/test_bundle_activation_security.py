import importlib.util
import pathlib
import sys
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOLS_SCRIPTS = REPO_ROOT / "tools" / "scripts"


def load_module(module_path: pathlib.Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


get_bundle_skills = load_module(
    TOOLS_SCRIPTS / "get-bundle-skills.py",
    "get_bundle_skills",
)


class BundleActivationSecurityTests(unittest.TestCase):
    def test_format_skills_for_batch_emits_newline_delimited_safe_ids(self):
        formatted = get_bundle_skills.format_skills_for_batch([
            "safe-skill",
            "nested.skill_2",
            "unsafe&calc",
            "another|bad",
        ])

        self.assertEqual(formatted, "safe-skill\nnested.skill_2\n")

    def test_get_bundle_skills_rejects_unsafe_bundle_entries(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            bundles_path = pathlib.Path(temp_dir) / "bundles.md"
            bundles_path.write_text(
                "\n".join(
                    [
                        "### Essentials",
                        "- [`safe-skill`](../../skills/safe-skill/)",
                        "- [`unsafe&calc`](../../skills/unsafe/)",
                        "- [`safe_two`](../../skills/safe_two/)",
                    ]
                ),
                encoding="utf-8",
            )

            skills = get_bundle_skills.get_bundle_skills(
                ["Essentials"],
                bundles_path=bundles_path,
            )

            self.assertEqual(skills, ["safe-skill", "safe_two"])


if __name__ == "__main__":
    unittest.main()
