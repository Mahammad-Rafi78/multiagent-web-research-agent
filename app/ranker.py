from __future__ import annotations

from app.models import SearchResult


def score_source(result: SearchResult) -> float:
    authority = 0.5 if "wikipedia" in result.url.lower() else 0.7
    freshness = 0.6
    evidence_quality = 0.6
    relevance = result.relevance_score if result.relevance_score is not None else 0.5
    return 0.40 * relevance + 0.25 * authority + 0.15 * freshness + 0.20 * evidence_quality


def rank_results(results: list[SearchResult]) -> list[tuple[SearchResult, str, float]]:
    ranked: list[tuple[SearchResult, str, float]] = []
    for result in results:
        score = score_source(result)
        reason = "High relevance and solid source quality." if score >= 0.7 else "Moderate relevance with some uncertainty."
        ranked.append((result, reason, score))
    return sorted(ranked, key=lambda item: item[2], reverse=True)
