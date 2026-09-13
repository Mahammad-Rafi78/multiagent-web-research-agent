from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.models import SearchQuery
from app.planner import plan_queries, validate_query


def test_plan_queries_generates_queries() -> None:
    queries = plan_queries("What are the advantages and limitations of RAG compared with fine-tuning?")
    assert len(queries) >= 1
    assert all(isinstance(q, SearchQuery) for q in queries)


def test_validate_query() -> None:
    assert validate_query(SearchQuery(text="RAG enterprise benefits")) is True
    assert validate_query(SearchQuery(text="")) is False
