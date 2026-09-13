from __future__ import annotations

import re
from typing import Any

import httpx
from bs4 import BeautifulSoup

from app.config import settings
from app.models import SourceDocument


class FetchError(RuntimeError):
    """Raised when a source cannot be fetched."""


def _extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for selector in ["article", "main", "body"]:
        block = soup.select_one(selector)
        if block:
            text = block.get_text(" ", strip=True)
            if len(text) > 100:
                return re.sub(r"\s+", " ", text)[:8000]
    text = soup.get_text(" ", strip=True)
    return re.sub(r"\s+", " ", text)[:8000]


def fetch_document(url: str, title: str = "Untitled", provider: str = "unknown") -> SourceDocument:
    client = httpx.Client(
        timeout=settings.REQUEST_TIMEOUT,
        follow_redirects=True,
        headers={"User-Agent": "Mozilla/5.0 (compatible; ResearchAgent/1.0)"},
    )
    try:
        response = client.get(url)
        response.raise_for_status()
        content = response.text
        text = _extract_text(content)
        if not text:
            raise FetchError("Empty webpage content")
        return SourceDocument(
            id=f"doc-{abs(hash(url)) % 1000000}",
            title=title,
            url=url,
            provider=provider,
            content=text,
            metadata={"status_code": response.status_code},
        )
    except (httpx.HTTPError, ValueError, FetchError) as exc:
        raise FetchError(f"Failed to fetch {url}: {exc}") from exc
    finally:
        client.close()
