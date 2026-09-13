from __future__ import annotations

from urllib.parse import parse_qsl, urlsplit, urlunsplit

from app.models import SearchResult


def normalize_url(raw_url: str) -> str:
    """Normalize URL for deduplication while preserving original form when possible."""
    if not raw_url:
        return ""
    parsed = urlsplit(raw_url)
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = parsed.path or "/"
    query_pairs = []
    for key, value in parse_qsl(parsed.query, keep_blank_values=True):
        if key.lower() in {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "fbclid", "msclkid", "mc_cid", "mc_eid"}:
            continue
        query_pairs.append((key, value))
    query = "&".join(f"{k}={v}" for k, v in query_pairs)
    fragment = ""
    normalized = urlunsplit((scheme, netloc, path.rstrip("/"), query, fragment))
    if not normalized.startswith(("http://", "https://")):
        return normalized
    return normalized.rstrip("/") if normalized != "http://" else normalized


def normalize_search_result(result: SearchResult) -> SearchResult:
    """Normalize fields like title, URL and snippet."""
    normalized = SearchResult.model_validate(result.model_dump())
    normalized.title = " ".join(normalized.title.split())
    normalized.snippet = " ".join(normalized.snippet.split())
    normalized.url = normalized.url.strip()
    normalized.normalized_url = normalize_url(normalized.url)
    return normalized
