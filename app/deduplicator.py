from __future__ import annotations

from collections import defaultdict

from app.models import SearchResult


def deduplicate_results(results: list[SearchResult]) -> tuple[list[SearchResult], list[SearchResult], dict[str, int]]:
    """Merge same URLs across providers and retain provenance."""
    by_key: dict[str, SearchResult] = {}
    duplicates: list[SearchResult] = []
    seen_urls: set[str] = set()

    for result in results:
        key = result.normalized_url or result.url
        if not key:
            continue
        if key in by_key:
            existing = by_key[key]
            if result.provider not in existing.discovered_by:
                existing.discovered_by.append(result.provider)
            if result.title and result.title not in existing.metadata.get("titles", []):
                existing.metadata.setdefault("titles", []).append(result.title)
            duplicates.append(result)
            continue
        result.discovered_by = [result.provider]
        if result.normalized_url is None:
            result.normalized_url = key
        by_key[key] = result

    unique_results = list(by_key.values())
    stats = {
        "unique": len(unique_results),
        "duplicates_removed": len(duplicates),
        "raw": len(results),
    }
    return unique_results, duplicates, stats
