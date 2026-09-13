from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.models import SearchResult
from app.normalizer import normalize_search_result, normalize_url


def test_normalize_url_removes_tracking_params() -> None:
    original = "https://example.com/page?utm_source=ad&utm_medium=web&x=1#frag"
    assert normalize_url(original) == "https://example.com/page?x=1"


def test_normalize_search_result() -> None:
    result = SearchResult(
        id="r1",
        title="  RAG Overview   ",
        url="https://example.com/page?utm_source=ad&x=1",
        snippet=" This is   a test. ",
        provider="brave",
        query="RAG",
    )
    normalized = normalize_search_result(result)
    assert normalized.title == "RAG Overview"
    assert normalized.snippet == "This is a test."
    assert normalized.normalized_url == "https://example.com/page?x=1"
