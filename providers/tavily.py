from __future__ import annotations

import logging
from typing import Any

import httpx

from app.config import settings
from app.models import SearchQuery, SearchResult
from app.normalizer import normalize_url
from providers.base import SearchProvider

logger = logging.getLogger(__name__)


class TavilySearchProvider(SearchProvider):
    name = "tavily"

    def __init__(self, client: httpx.Client | None = None) -> None:
        self.client = client or httpx.Client(timeout=settings.REQUEST_TIMEOUT)

    def search(self, query: SearchQuery, *, limit: int = 5) -> list[SearchResult]:
        if not settings.has_tavily:
            raise ValueError("TAVILY_API_KEY is not configured.")

        url = "https://api.tavily.com/search"
        payload = {
            "api_key": settings.TAVILY_API_KEY,
            "query": query.text,
            "max_results": limit,
            "search_depth": "basic",
            "include_answer": False,
            "include_raw_content": False,
        }

        response = self.client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])

        normalized: list[SearchResult] = []
        for index, item in enumerate(results[:limit]):
            title = str(item.get("title") or "Untitled").strip()
            url_value = str(item.get("url") or "").strip()
            snippet = str(item.get("content") or item.get("snippet") or "").strip()
            normalized_url = normalize_url(url_value)
            result = SearchResult(
                id=f"{self.name}-{index}-{hash(normalized_url or url_value) % 100000}",
                title=title,
                url=url_value,
                snippet=snippet,
                provider=self.name,
                query=query.text,
                published_date=item.get("published_date"),
                relevance_score=float(item.get("score", 0.0) or 0.0),
                metadata={"raw": item},
                normalized_url=normalized_url,
                discovered_by=[self.name],
            )
            normalized.append(result)
        return normalized
