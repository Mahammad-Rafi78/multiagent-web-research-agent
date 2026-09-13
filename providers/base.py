from __future__ import annotations

from abc import ABC, abstractmethod

from app.models import SearchQuery, SearchResult


class SearchProvider(ABC):
    """Abstract interface for search providers."""

    name: str

    @abstractmethod
    def search(self, query: SearchQuery, *, limit: int = 5) -> list[SearchResult]:
        """Return normalized results for a query."""
