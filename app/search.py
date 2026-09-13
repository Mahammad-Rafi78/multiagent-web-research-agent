from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

from app.config import settings
from app.logging_config import get_logger
from app.models import ProviderStatus, ResearchRun, SearchQuery, SearchResult
from app.normalizer import normalize_search_result
from providers.base import SearchProvider
from providers.brave import BraveSearchProvider
from providers.tavily import TavilySearchProvider

logger = get_logger(__name__)


class SearchOrchestrator:
    """Query multiple independent providers and merge results safely."""

    def __init__(self, providers: list[SearchProvider] | None = None) -> None:
        self.providers = providers or [TavilySearchProvider(), BraveSearchProvider()]

    def query_all(self, queries: list[SearchQuery]) -> tuple[list[SearchResult], ResearchRun]:
        merged: list[SearchResult] = []
        provider_status: list[ProviderStatus] = []
        errors: list[str] = []

        for query in queries:
            if not query.text.strip():
                continue

            for provider in self.providers:
                try:
                    logger.info("Querying provider %s for %s", provider.name, query.text)
                    results = provider.search(query, limit=min(5, settings.MAX_SEARCH_RESULTS))
                    normalized = [normalize_search_result(item) for item in results]
                    merged.extend(normalized)
                    provider_status.append(
                        ProviderStatus(provider=provider.name, status="success", attempts=1, results=len(normalized))
                    )
                except Exception as exc:  # recoverable
                    status = ProviderStatus(provider=provider.name, status="failed", attempts=1, error=str(exc))
                    provider_status.append(status)
                    errors.append(f"{provider.name}: {exc}")
                    logger.warning("Provider failed for %s: %s", query.text, exc)

        run = ResearchRun(
            question=" ".join(q.text for q in queries),
            queries=[q.text for q in queries],
            providers_attempted=[p.name for p in self.providers],
            successful_providers=sorted({status.provider for status in provider_status if status.status == "success"}),
            failed_providers=sorted({status.provider for status in provider_status if status.status == "failed"}),
            raw_result_count=len(merged),
            deduplicated_result_count=len(merged),
            errors=errors,
            provider_status=provider_status,
        )
        return merged, run
