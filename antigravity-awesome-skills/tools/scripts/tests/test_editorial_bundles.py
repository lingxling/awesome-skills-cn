import importlib.util
import pathlib
import sys
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOLS_SCRIPTS = REPO_ROOT / "tools" / "scripts"


def load_module(module_path: pathlib.Path, module_name: str):
    sys.path.insert(0, str(module_path.parent))
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


editorial_bundles = load_module(
    TOOLS_SCRIPTS / "sync_editorial_bundles.py",
    "sync_editorial_bundles",
)
plugin_compatibility = load_module(
    TOOLS_SCRIPTS / "plugin_compatibility.py",
    "plugin_compatibility_json",
)
get_bundle_skills = load_module(
    TOOLS_SCRIPTS / "get-bundle-skills.py",
    "get_bundle_skills_json",
)


class EditorialBundlesTests(unittest.TestCase):
    def setUp(self):
        self.manifest_bundles = editorial_bundles.load_editorial_bundles(REPO_ROOT)
        self.compatibility_report = plugin_compatibility.load_plugin_compatibility(REPO_ROOT)
        self.compatibility_by_id = plugin_compatibility.compatibility_by_skill_id(self.compatibility_report)

    def test_manifest_has_unique_ids_and_existing_skills(self):
        bundle_ids = [bundle["id"] for bundle in self.manifest_bundles]
        self.assertEqual(len(bundle_ids), len(set(bundle_ids)))

        for bundle in self.manifest_bundles:
            self.assertEqual(bundle["id"], get_bundle_skills._normalize_bundle_query(bundle["name"]))
            self.assertTrue(bundle["skills"], f'bundle "{bundle["id"]}" should not be empty')
            for skill in bundle["skills"]:
                self.assertTrue((REPO_ROOT / "skills" / skill["id"]).exists())

    def test_bundles_doc_matches_renderer(self):
        metadata = editorial_bundles.load_metadata(str(REPO_ROOT))
        expected = editorial_bundles.render_bundles_doc(
            REPO_ROOT,
            metadata,
            self.manifest_bundles,
            self.compatibility_by_id,
        )
        actual = (REPO_ROOT / "docs" / "users" / "bundles.md").read_text(encoding="utf-8")
        self.assertEqual(actual, expected)

    def test_get_bundle_skills_reads_json_manifest_by_name_and_id(self):
        expected = ["concise-planning", "git-pushing", "kaizen", "lint-and-validate", "systematic-debugging"]
        self.assertEqual(get_bundle_skills.get_bundle_skills(["Essentials"]), expected)
        self.assertEqual(get_bundle_skills.get_bundle_skills(["essentials"]), expected)
        web_wizard_skills = get_bundle_skills.get_bundle_skills(["web-wizard"])
        self.assertIn("form-cro", web_wizard_skills)
        self.assertIn("react-best-practices", web_wizard_skills)
        self.assertIn(
            "game-development/game-design",
            get_bundle_skills.get_bundle_skills(["indie-game-dev"]),
        )

    def test_generated_bundle_plugin_contains_expected_skills(self):
        essentials_plugin = REPO_ROOT / "plugins" / "antigravity-bundle-essentials" / "skills"
        expected_ids = {
            skill["id"]
            for skill in next(bundle for bundle in self.manifest_bundles if bundle["id"] == "essentials")["skills"]
        }
        actual_ids = {
            str(path.relative_to(essentials_plugin))
            for path in essentials_plugin.rglob("SKILL.md")
        }
        self.assertEqual(actual_ids, {f"{skill_id}/SKILL.md" for skill_id in expected_ids})

        sample_skill_dir = essentials_plugin / "concise-planning"
        self.assertTrue((sample_skill_dir / "SKILL.md").is_file())

    def test_generated_plugin_count_matches_manifest(self):
        generated_plugins = sorted(
            path.name
            for path in (REPO_ROOT / "plugins").iterdir()
            if path.is_dir() and path.name.startswith("antigravity-bundle-")
        )
        expected_plugins = sorted(
            f'antigravity-bundle-{bundle["id"]}'
            for bundle in self.manifest_bundles
            if any(
                all(
                    self.compatibility_by_id[skill["id"]]["targets"][target] == "supported"
                    for skill in bundle["skills"]
                )
                for target in ("codex", "claude")
            )
        )
        self.assertEqual(generated_plugins, expected_plugins)

    def test_sample_bundle_copy_matches_source_file_inventory(self):
        sample_bundle = next(bundle for bundle in self.manifest_bundles if bundle["id"] == "documents-presentations")
        plugin_skills_root = REPO_ROOT / "plugins" / "antigravity-bundle-documents-presentations" / "skills"

        for skill in sample_bundle["skills"]:
            source_dir = REPO_ROOT / "skills" / skill["id"]
            copied_dir = plugin_skills_root / skill["id"]
            self.assertTrue(copied_dir.is_dir(), f'copied skill dir missing for {skill["id"]}')

            source_files = sorted(
                str(path.relative_to(source_dir))
                for path in source_dir.rglob("*")
                if path.is_file()
            )
            copied_files = sorted(
                str(path.relative_to(copied_dir))
                for path in copied_dir.rglob("*")
                if path.is_file()
            )
            self.assertEqual(copied_files, source_files, f'copied bundle skill should match source inventory for {skill["id"]}')

    def test_root_plugins_only_include_supported_skills_for_target(self):
        codex_root = REPO_ROOT / "plugins" / "antigravity-awesome-skills" / "skills"
        claude_root = REPO_ROOT / "plugins" / "antigravity-awesome-skills-claude" / "skills"

        for skill_id, compatibility in self.compatibility_by_id.items():
            codex_path = codex_root / skill_id
            claude_path = claude_root / skill_id
            self.assertEqual(
                codex_path.exists(),
                compatibility["targets"]["codex"] == "supported",
                f"Codex root plugin inclusion mismatch for {skill_id}",
            )
            self.assertEqual(
                claude_path.exists(),
                compatibility["targets"]["claude"] == "supported",
                f"Claude root plugin inclusion mismatch for {skill_id}",
            )


if __name__ == "__main__":
    unittest.main()
