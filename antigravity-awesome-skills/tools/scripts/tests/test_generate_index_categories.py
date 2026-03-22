import importlib.util
import pathlib
import sys
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "tools" / "scripts"))


def load_module(module_path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, REPO_ROOT / module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


generate_index = load_module("tools/scripts/generate_index.py", "generate_index_categories")


class GenerateIndexCategoryTests(unittest.TestCase):
    def test_normalize_category_preserves_specialized_labels(self):
        self.assertEqual(generate_index.normalize_category(" Front-End "), "front-end")
        self.assertEqual(generate_index.normalize_category("Ai-Agents"), "ai-agents")
        self.assertEqual(generate_index.normalize_category("Document-Processing"), "document-processing")

    def test_infer_category_returns_none_for_weak_signal(self):
        inferred = generate_index.infer_category(
            "mystery-skill",
            "Mystery Skill",
            "General-purpose guidance for assorted tasks.",
        )
        self.assertIsNone(inferred)

    def test_infer_category_detects_security_skill(self):
        inferred = generate_index.infer_category(
            "web-security-testing",
            "Web Security Testing",
            "Identify vulnerabilities, auth flaws, and threat scenarios for web applications.",
        )
        self.assertEqual(inferred, "security")

    def test_infer_category_uses_family_prefix_when_high_confidence(self):
        inferred = generate_index.infer_category(
            "apify-market-research",
            "Apify Market Research",
            "Research markets using Apify actors.",
        )
        self.assertEqual(inferred, "automation")

    def test_infer_category_maps_workflow_family_prefixes(self):
        inferred = generate_index.infer_category(
            "github-actions-templates",
            "GitHub Actions Templates",
            "Production-ready workflow patterns for GitHub automation.",
        )
        self.assertEqual(inferred, "workflow")

    def test_infer_category_maps_development_family_prefixes(self):
        inferred = generate_index.infer_category(
            "javascript-mastery",
            "JavaScript Mastery",
            "Essential JavaScript concepts for developers.",
        )
        self.assertEqual(inferred, "development")

    def test_generate_index_prefers_frontmatter_then_parent_then_inference(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = pathlib.Path(temp_dir)
            skills_dir = base / "skills"
            output_file = base / "skills_index.json"

            explicit_dir = skills_dir / "explicit-skill"
            explicit_dir.mkdir(parents=True)
            (explicit_dir / "SKILL.md").write_text(
                "---\nname: explicit-skill\ncategory: custom\n---\nbody\n",
                encoding="utf-8",
            )

            nested_dir = skills_dir / "bundles" / "nested-skill"
            nested_dir.mkdir(parents=True)
            (nested_dir / "SKILL.md").write_text(
                "---\nname: nested-skill\ndescription: Example\n---\nbody\n",
                encoding="utf-8",
            )

            inferred_dir = skills_dir / "playwright-skill"
            inferred_dir.mkdir(parents=True)
            (inferred_dir / "SKILL.md").write_text(
                "---\nname: playwright-skill\ndescription: End-to-end test automation with Playwright and browser workflows.\n---\nbody\n",
                encoding="utf-8",
            )

            skills = generate_index.generate_index(str(skills_dir), str(output_file))
            categories = {skill["id"]: skill["category"] for skill in skills}

            self.assertEqual(categories["explicit-skill"], "custom")
            self.assertEqual(categories["nested-skill"], "bundles")
            self.assertEqual(categories["playwright-skill"], "test-automation")

    def test_generate_index_preserves_explicit_specialized_category(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = pathlib.Path(temp_dir)
            skills_dir = base / "skills"
            output_file = base / "skills_index.json"

            legacy_dir = skills_dir / "legacy-skill"
            legacy_dir.mkdir(parents=True)
            (legacy_dir / "SKILL.md").write_text(
                "---\nname: legacy-skill\ncategory: front-end\ndescription: Example\n---\nbody\n",
                encoding="utf-8",
            )

            skills = generate_index.generate_index(str(skills_dir), str(output_file))
            self.assertEqual(skills[0]["category"], "front-end")

    def test_generate_index_applies_curated_override(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = pathlib.Path(temp_dir)
            skills_dir = base / "skills"
            output_file = base / "skills_index.json"

            override_dir = skills_dir / "playwright-skill"
            override_dir.mkdir(parents=True)
            (override_dir / "SKILL.md").write_text(
                "---\nname: playwright-skill\ncategory: custom\ndescription: Browser automation\n---\nbody\n",
                encoding="utf-8",
            )

            skills = generate_index.generate_index(str(skills_dir), str(output_file))
            self.assertEqual(skills[0]["category"], "test-automation")

    def test_generate_index_applies_specialist_override(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = pathlib.Path(temp_dir)
            skills_dir = base / "skills"
            output_file = base / "skills_index.json"

            override_dir = skills_dir / "design-spells"
            override_dir.mkdir(parents=True)
            (override_dir / "SKILL.md").write_text(
                "---\nname: design-spells\ndescription: Curated micro-interactions and design details.\n---\nbody\n",
                encoding="utf-8",
            )

            skills = generate_index.generate_index(str(skills_dir), str(output_file))
            self.assertEqual(skills[0]["category"], "design")

    def test_generate_index_applies_curated_domain_overrides(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = pathlib.Path(temp_dir)
            skills_dir = base / "skills"
            output_file = base / "skills_index.json"

            fixtures = {
                "commit": "workflow",
                "activecampaign-automation": "marketing",
                "datadog-automation": "reliability",
                "business-analyst": "business",
                "zod-validation-expert": "framework",
                "architect-review": "architecture",
                "family-health-analyzer": "health",
                "astropy": "science",
            }

            for skill_id in fixtures:
                override_dir = skills_dir / skill_id
                override_dir.mkdir(parents=True)
                (override_dir / "SKILL.md").write_text(
                    f"---\nname: {skill_id}\ncategory: custom\ndescription: Example\n---\nbody\n",
                    encoding="utf-8",
                )

            skills = generate_index.generate_index(str(skills_dir), str(output_file))
            categories = {skill["id"]: skill["category"] for skill in skills}

            for skill_id, category in fixtures.items():
                self.assertEqual(categories[skill_id], category)


if __name__ == "__main__":
    unittest.main()
