"""Regression tests for the Parallel-first research lookup skill."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "skills" / "research-lookup" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from manuscript_packet import (  # noqa: E402
    build_manuscript_packet,
    deduplicate_sources,
    save_packet,
)
from research_lookup import (  # noqa: E402
    DEFAULT_TARGET_REFERENCES,
    ResearchLookup,
    build_parser,
)


def source(
    index: int,
    *,
    title: str | None = None,
    text: str | None = None,
    extracted: bool = False,
) -> dict:
    return {
        "title": title or f"Randomized controlled trial of intervention {index}",
        "url": f"https://pubmed.ncbi.nlm.nih.gov/{1000000 + index}/",
        "publish_date": f"202{index % 6}-01-01",
        "excerpts": [
            text
            or (
                f"Authors: Author {index}. Journal: Evidence Journal. PMID: "
                f"{1000000 + index}. Randomized controlled trial. n={100 + index}. "
                "The study showed a 20% improvement (p<0.05). "
                "A limitation was the short follow-up."
            )
        ],
        "extracted": extracted,
    }


class RoutingTests(unittest.TestCase):
    @patch("research_lookup.shutil.which", return_value="/usr/local/bin/parallel-cli")
    def test_default_backend_is_search_and_parallel_alias_is_research(self, _which):
        default = ResearchLookup()
        legacy = ResearchLookup(force_backend="parallel")

        self.assertEqual(default._select_backend("general research"), "search")
        self.assertEqual(legacy._select_backend("deep research"), "research")

    @patch("research_lookup.shutil.which", return_value="/usr/local/bin/parallel-cli")
    @patch.dict("research_lookup.os.environ", {"PARALLEL_API_KEY": "test-key"})
    def test_chat_is_available_but_never_selected_by_default(self, _which):
        default = ResearchLookup()
        explicit = ResearchLookup(force_backend="chat", chat_model="core")

        self.assertEqual(default._select_backend("synthesize evidence"), "search")
        self.assertEqual(explicit._select_backend("synthesize evidence"), "chat")

    @patch("research_lookup.shutil.which", return_value="/usr/local/bin/parallel-cli")
    @patch.dict("research_lookup.os.environ", {"PARALLEL_API_KEY": "test-key"})
    def test_explicit_chat_preserves_content_basis_and_citations(self, _which):
        lookup = ResearchLookup(force_backend="chat", chat_model="core")

        class FakeResponse:
            def raise_for_status(self):
                return None

            def json(self):
                return {
                    "choices": [
                        {
                            "message": {
                                "content": (
                                    "Evidence synthesis with DOI: 10.1234/example."
                                )
                            }
                        }
                    ],
                    "basis": [
                        {
                            "citations": [
                                {
                                    "title": "Basis source",
                                    "url": "https://example.org/source",
                                }
                            ]
                        }
                    ],
                    "usage": {"total_tokens": 100},
                }

        with patch("requests.post", return_value=FakeResponse()) as post:
            result = lookup.lookup("synthesize the evidence")

        self.assertTrue(result["success"])
        self.assertEqual(result["backend"], "chat")
        self.assertEqual(result["model"], "parallel-chat/core")
        self.assertEqual(result["sources"][0]["title"], "Basis source")
        self.assertTrue(
            any(
                citation["url"] == "https://doi.org/10.1234/example"
                for citation in result["citations"]
            )
        )
        request = post.call_args
        self.assertEqual(
            request.args[0], "https://api.parallel.ai/chat/completions"
        )
        self.assertEqual(request.kwargs["json"]["model"], "core")
        self.assertFalse(request.kwargs["json"]["stream"])

    @patch("research_lookup.shutil.which", return_value="/usr/local/bin/parallel-cli")
    def test_parser_and_class_default_to_sixty_references(self, _which):
        args = build_parser().parse_args(
            ["topic", "--academic", "--force-backend", "chat"]
        )
        lookup = ResearchLookup(academic=True)

        self.assertEqual(DEFAULT_TARGET_REFERENCES, 60)
        self.assertEqual(args.target_references, 60)
        self.assertEqual(args.force_backend, "chat")
        self.assertEqual(args.chat_model, "core")
        self.assertEqual(lookup.target_references, 60)
        self.assertEqual(lookup.extract_limit, 60)

    @patch("research_lookup.shutil.which", return_value="/usr/local/bin/parallel-cli")
    def test_nonacademic_lookup_uses_one_search_without_extract(self, _which):
        lookup = ResearchLookup(academic=False, max_results=2)
        calls: list[list[str]] = []

        def fake_cli(args, *, timeout=None):
            del timeout
            calls.append(args)
            return {
                "search_id": "search_general",
                "session_id": "session_general",
                "status": "ok",
                "results": [source(1), source(2)],
                "usage": [{"name": "sku_search", "count": 1}],
            }

        lookup._run_parallel_cli = fake_cli  # type: ignore[method-assign]
        result = lookup.lookup("latest official technical guidance")

        self.assertTrue(result["success"])
        self.assertEqual(result["backend"], "search")
        self.assertFalse(result["academic"])
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][0], "search")
        self.assertEqual(result["usage"], [{"name": "sku_search", "count": 1}])

    @patch("research_lookup.shutil.which", return_value="/usr/local/bin/parallel-cli")
    def test_academic_lookup_runs_facets_and_batched_extract(self, _which):
        lookup = ResearchLookup(
            academic=True,
            target_references=3,
            max_results=2,
            extract_limit=3,
            extract_batch_size=2,
        )
        search_count = 0
        extract_count = 0

        def fake_cli(args, *, timeout=None):
            nonlocal search_count, extract_count
            del timeout
            if args[0] == "search":
                search_count += 1
                start = search_count * 10
                return {
                    "search_id": f"search_{search_count}",
                    "session_id": "session_academic",
                    "status": "ok",
                    "results": [source(start), source(start + 1)],
                    "usage": [{"name": "sku_search", "count": 1}],
                }
            self.assertEqual(args[0], "extract")
            extract_count += 1
            urls = [
                value
                for value in args[1 : args.index("--objective")]
                if value.startswith("https://")
            ]
            return {
                "extract_id": f"extract_{extract_count}",
                "session_id": "session_academic",
                "status": "ok",
                "results": [
                    {
                        **source(int(url.rstrip("/").split("/")[-1]) - 1000000),
                        "url": url,
                    }
                    for url in urls
                ],
                "errors": [],
                "usage": [{"name": "sku_extract_excerpts", "count": len(urls)}],
            }

        lookup._run_parallel_cli = fake_cli  # type: ignore[method-assign]
        result = lookup.lookup("find papers for a manuscript on intervention")

        self.assertTrue(result["success"])
        self.assertTrue(result["academic"])
        self.assertEqual(search_count, 5)
        self.assertEqual(extract_count, 2)
        self.assertEqual(result["packet"]["target_references"], 3)
        self.assertGreaterEqual(len(result["packet"]["references"]), 3)
        self.assertGreaterEqual(
            result["packet"]["coverage"]["verified_references"],
            3,
        )
        self.assertEqual(
            result["packet"]["coverage"]["verification_mix"]["extracted"],
            3,
        )
        self.assertIn("search_ledger", result)
        self.assertTrue(
            any(entry["capability"] == "extract" for entry in result["search_ledger"])
        )

    @patch("research_lookup.shutil.which", return_value="/usr/local/bin/parallel-cli")
    @patch.dict("research_lookup.os.environ", {"OPENROUTER_API_KEY": "test-key"})
    def test_perplexity_failure_fallback_is_opt_in(self, _which):
        lookup = ResearchLookup(allow_perplexity_fallback=True)
        lookup._parallel_search = lambda query: (_ for _ in ()).throw(  # type: ignore[method-assign]
            RuntimeError("search unavailable")
        )
        lookup._perplexity_lookup = lambda query: {  # type: ignore[method-assign]
            "success": True,
            "query": query,
            "response": "fallback",
            "citations": [],
            "sources": [],
            "timestamp": "now",
            "backend": "perplexity",
            "model": "perplexity/sonar-pro-search",
        }

        result = lookup.lookup("topic")

        self.assertTrue(result["success"])
        self.assertEqual(result["fallback_from"], "search")
        self.assertIn("search unavailable", result["fallback_reason"])


class PacketTests(unittest.TestCase):
    def test_deduplication_merges_doi_url_and_title_records(self):
        first = {
            "title": "A Definitive Study",
            "url": "https://doi.org/10.1234/example?utm_source=test",
            "excerpts": ["DOI: 10.1234/example"],
            "facets": ["reviews"],
        }
        duplicate = {
            "title": "A definitive study",
            "url": "https://doi.org/10.1234/example",
            "excerpts": ["Additional evidence."],
            "facets": ["seminal"],
            "extracted": True,
        }

        merged = deduplicate_sources([first, duplicate])

        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["doi"], "10.1234/example")
        self.assertEqual(merged[0]["facets"], ["reviews", "seminal"])
        self.assertTrue(merged[0]["extracted"])
        self.assertEqual(len(merged[0]["excerpts"]), 2)

    def test_packet_has_manuscript_artifacts_and_never_pads_shortfall(self):
        sources = [
            source(1, extracted=True),
            source(
                2,
                text=(
                    "Authors: Researcher Two. Journal: Evidence Journal. "
                    "PMID: 1000002. Systematic review. The evidence was inconsistent "
                    "and showed no significant effect. Limitation: high heterogeneity."
                ),
                extracted=True,
            ),
        ]

        packet = build_manuscript_packet(
            query="manuscript evidence",
            sources=sources,
            search_ledger=[{"capability": "search", "status": "ok"}],
            target_references=60,
            manuscript_context={"study_type": "cohort"},
        )

        self.assertEqual(len(packet["references"]), 2)
        self.assertEqual(packet["coverage"]["requested_references"], 60)
        self.assertEqual(packet["coverage"]["verified_references"], 2)
        self.assertEqual(packet["coverage"]["shortfall"], 58)
        self.assertTrue(packet["claim_source_map"])
        self.assertIn("introduction", packet["section_briefs"])
        self.assertIn("methods-rationale", packet["section_briefs"])
        self.assertIn("discussion", packet["section_briefs"])
        self.assertTrue(packet["synthesis"]["conflicting_evidence"])
        self.assertTrue(any("not padded" in item for item in packet["warnings"]))

    def test_retracted_reference_is_marked_for_exclusion(self):
        packet = build_manuscript_packet(
            query="topic",
            sources=[
                source(
                    1,
                    text=(
                        "Retraction notice. This randomized controlled trial was "
                        "retracted because the findings were unreliable."
                    ),
                    extracted=True,
                )
            ],
            search_ledger=[],
            target_references=1,
        )

        reference = packet["references"][0]
        self.assertTrue(reference["retracted"])
        self.assertEqual(reference["evidence_quality"], "exclude")
        self.assertEqual(packet["coverage"]["verified_references"], 0)
        self.assertEqual(packet["claim_source_map"], [])

    def test_save_packet_writes_all_expected_artifacts(self):
        packet = build_manuscript_packet(
            query="topic",
            sources=[source(1, extracted=True)],
            search_ledger=[{"capability": "search", "status": "ok"}],
            target_references=1,
        )

        with tempfile.TemporaryDirectory() as directory:
            artifacts = save_packet(packet, directory)

            self.assertEqual(
                set(artifacts),
                {
                    "packet_json",
                    "packet_markdown",
                    "references_json",
                    "references_bib",
                    "evidence_matrix",
                    "claim_source_map",
                    "synthesis",
                    "section_briefs",
                    "coverage",
                    "search_ledger",
                },
            )
            self.assertTrue(all(Path(path).exists() for path in artifacts.values()))
            self.assertIn(
                "Manuscript Research Packet",
                Path(artifacts["packet_markdown"]).read_text(encoding="utf-8"),
            )

    def test_existing_citation_extraction_remains_available(self):
        citations = ResearchLookup._extract_citations_from_text(
            "See DOI: 10.1234/Example and https://pubmed.ncbi.nlm.nih.gov/12345678/."
        )
        urls = {citation["url"] for citation in citations}

        self.assertIn("https://doi.org/10.1234/example", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/12345678", urls)


if __name__ == "__main__":
    unittest.main()
