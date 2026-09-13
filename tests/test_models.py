from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.models import ResearchQuestion, SearchQuery, SearchResult


def test_research_question_model() -> None:
    question = ResearchQuestion(question="What is RAG?")
    assert question.question == "What is RAG?"


def test_search_query_model() -> None:
    query = SearchQuery(text="RAG enterprise benefits")
    assert query.text == "RAG enterprise benefits"


def test_search_result_model() -> None:
    result = SearchResult(
        id="r1",
        title="RAG Overview",
        url="https://example.com/rag",
        provider="tavily",
        query="RAG",
    )
    assert result.provider == "tavily"
    assert result.id == "r1"
