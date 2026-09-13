from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.deduplicator import deduplicate_results
from app.models import SearchResult


def test_deduplicate_results_by_normalized_url() -> None:
    results = [
        SearchResult(id="A", title="Alpha", url="https://example.com/a?utm_source=x", provider="tavily", query="q", normalized_url="https://example.com/a"),
        SearchResult(id="B", title="Alpha 2", url="https://example.com/a", provider="brave", query="q", normalized_url="https://example.com/a"),
    ]
    unique, duplicates, stats = deduplicate_results(results)
    assert len(unique) == 1
    assert len(duplicates) == 1
    assert unique[0].discovered_by == ["tavily", "brave"]
    assert stats["duplicates_removed"] == 1
