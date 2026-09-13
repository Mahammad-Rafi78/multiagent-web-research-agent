from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.models import SearchResult
from app.ranker import rank_results, score_source


def test_score_source_returns_float() -> None:
    result = SearchResult(id="r1", title="Official docs", url="https://example.com/docs", provider="tavily", query="RAG", relevance_score=0.9)
    assert score_source(result) > 0


def test_rank_results_orders_by_score() -> None:
    a = SearchResult(id="a", title="A", url="https://example.com/a", provider="tavily", query="RAG", relevance_score=0.9)
    b = SearchResult(id="b", title="B", url="https://example.com/b", provider="brave", query="RAG", relevance_score=0.3)
    ordered = rank_results([b, a])
    assert ordered[0][0].id == "a"
