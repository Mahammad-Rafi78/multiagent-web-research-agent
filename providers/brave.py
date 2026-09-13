from __future__ import annotations

import logging
from typing import Any

import httpx

from app.config import settings
from app.models import SearchQuery, SearchResult
from app.normalizer import normalize_url
from providers.base import SearchProvider

logger = logging.getLogger(__name__)


class BraveSearchProvider(SearchProvider):
    name = "brave"

    def __init__(self, client: httpx.Client | None = None) -> None:
        self.client = client or httpx.Client(timeout=settings.REQUEST_TIMEOUT)

    def search(self, query: SearchQuery, *, limit: int = 5) -> list[SearchResult]:
        if not settings.has_brave:
            raise ValueError("BRAVE_API_KEY is not configured.")

        params = {
            "q": query.text,
            "count": limit,
            "country": "US",
            "search_lang": "en",
            "safesearch": "moderate",
            "result_filter": "web",
            "text_decorations": "false",
        }
        headers = {"X-Subscription-Token": settings.BRAVE_API_KEY}
        response = self.client.get("https://api.search.brave.com/res/v1/web/search", params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        results = data.get("web", {}).get("results", [])

        normalized: list[SearchResult] = []
        for index, item in enumerate(results[:limit]):
            title = str(item.get("title") or "Untitled").strip()
            url_value = str(item.get("url") or "").strip()
            snippet = str(item.get("description") or "").strip()
            result = SearchResult(
                id=f"{self.name}-{index}-{hash(url_value) % 100000}",
                title=title,
                url=url_value,
                snippet=snippet,
                provider=self.name,
                query=query.text,
                published_date=item.get("published") or item.get("date") or None,
                relevance_score=float(item.get("score", 0.0) or 0.0),
                metadata={"raw": item},
                normalized_url=normalize_url(url_value),
                discovered_by=[self.name],
            )
            normalized.append(result)
        return normalized
