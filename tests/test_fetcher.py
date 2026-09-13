from __future__ import annotations

import sys
from pathlib import Path

import httpx
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.fetcher import FetchError, fetch_document


def test_fetch_document_success(monkeypatch) -> None:
    class DummyResponse:
        status_code = 200
        text = "<html><body><main>Retrieval augmented generation can reduce hallucinations.</main></body></html>"

        def raise_for_status(self):
            return None

    class DummyClient:
        def __init__(self, *args, **kwargs):
            pass

        def get(self, url):
            return DummyResponse()

        def close(self):
            return None

    monkeypatch.setattr(httpx, "Client", DummyClient)
    doc = fetch_document("https://example.com")
    assert "Retrieval" in doc.content


def test_fetch_document_failure_raises() -> None:
    with pytest.raises(FetchError):
        fetch_document("https://example.invalid")
