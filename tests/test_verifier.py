from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.models import Claim, Evidence
from app.verifier import verify_claim


def test_verify_claim_supported() -> None:
    claim = Claim(id="c1", text="RAG helps with freshness.")
    ev = [
        Evidence(id="e1", source_id="s1", source_url="https://example.com", source_title="Source", passage="RAG improves freshness.", relevance_reason="direct", provider="tavily", question="What is RAG?"),
        Evidence(id="e2", source_id="s2", source_url="https://example.org", source_title="Source 2", passage="RAG helps keep information current.", relevance_reason="direct", provider="brave", question="What is RAG?"),
    ]
    result = verify_claim(claim, ev)
    assert result.status == "supported"


def test_verify_claim_insufficient() -> None:
    claim = Claim(id="c2", text="RAG always works.")
    result = verify_claim(claim, [])
    assert result.status == "insufficient_evidence"
