from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.conflicts import detect_conflicts
from app.models import Evidence


def test_detect_conflicts() -> None:
    evidence = [
        Evidence(id="e1", source_id="s1", source_url="https://example.com/a", source_title="A", passage="RAG reduces hallucinations.", relevance_reason="direct", provider="tavily", question="What is RAG?"),
        Evidence(id="e2", source_id="s2", source_url="https://example.com/b", source_title="B", passage="RAG does not reduce hallucinations.", relevance_reason="direct", provider="brave", question="What is RAG?"),
    ]
    result = detect_conflicts(evidence)
    assert len(result) >= 1
