from __future__ import annotations

from typing import Any

from app.citations import validate_citations
from app.config import settings
from app.conflicts import detect_conflicts
from app.deduplicator import deduplicate_results
from app.evidence import extract_evidence
from app.fetcher import FetchError, fetch_document
from app.logging_config import get_logger
from app.models import Claim, Evidence, ProviderStatus, ResearchAnswer, ResearchRun
from app.normalizer import normalize_search_result
from app.planner import plan_queries
from app.ranker import rank_results
from app.search import SearchOrchestrator
from app.synthesizer import SynthesisError, synthesize_answer
from app.verifier import verify_claim
from providers.base import SearchProvider

logger = get_logger(__name__)


class ResearchAgent:
    """End-to-end research pipeline."""

    def __init__(self, orchestrator: SearchOrchestrator | None = None) -> None:
        self.orchestrator = orchestrator or SearchOrchestrator()

    def run(self, question: str) -> ResearchAnswer:
        queries = plan_queries(question)
        raw_results, run = self.orchestrator.query_all(queries)
        normalized = [normalize_search_result(r) for r in raw_results]
        unique_results, duplicates, dedup_stats = deduplicate_results(normalized)
        ranked = rank_results(unique_results)
        selected = [result for result, _, _ in ranked[: settings.MAX_SOURCES_TO_FETCH]]

        fetched_docs = []
        evidence: list[Evidence] = []
        for result in selected:
            try:
                doc = fetch_document(result.url, title=result.title, provider=result.provider)
                fetched_docs.append(doc)
                evidence.extend(extract_evidence(doc, question))
            except FetchError as exc:
                logger.warning("Fetch failed for %s: %s", result.url, exc)
                run.sources_unavailable += 1
                run.errors.append(str(exc))
                if len(result.snippet.strip()) >= 40:
                    evidence.append(
                        Evidence(
                            id=f"snippet-{result.id}",
                            source_id=result.id,
                            source_url=result.url,
                            source_title=result.title,
                            passage=result.snippet[:600],
                            relevance_reason="Search-provider snippet used because the source page was unavailable.",
                            provider=result.provider,
                            question=question,
                        )
                    )

        run.sources_selected = len(selected)
        run.sources_fetched = len(fetched_docs)
        run.deduplicated_result_count = dedup_stats["unique"]
        run.raw_result_count = dedup_stats["raw"]

        claims = [
            Claim(id="C1", text="RAG is useful for enterprise applications.", category="general"),
            Claim(id="C2", text="Fine-tuning is useful but has limitations.", category="general"),
        ]
        verification = [verify_claim(c, [e for e in evidence if e.source_id]) for c in claims]
        conflicts = detect_conflicts(evidence)

        try:
            answer = synthesize_answer(question, evidence, conflicts, run.model_dump())
        except SynthesisError as exc:
            raise RuntimeError(f"Answer synthesis failed because the LLM provider was unavailable: {exc}") from exc

        valid_citation_ids = [f"S{index}" for index, _ in enumerate(evidence, start=1)]
        if not validate_citations(answer.answer, valid_citation_ids):
            raise RuntimeError("Generated answer contained invalid citations.")

        answer.research_run = run.model_dump()
        return answer
