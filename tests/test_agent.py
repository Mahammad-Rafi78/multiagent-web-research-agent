from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.agent import ResearchAgent
from app.models import SearchQuery, SearchResult


class DummyProvider:
    name = "dummy"

    def search(self, query: SearchQuery, *, limit: int = 5):
        return [
            SearchResult(
                id="dummy-1",
                title="Dummy source",
                url="https://example.com/dummy",
                snippet="This source explains how RAG can reduce hallucinations.",
                provider=self.name,
                query=query.text,
                relevance_score=0.8,
                normalized_url="https://example.com/dummy",
            )
        ]


def test_agent_runs_pipeline(monkeypatch) -> None:
    agent = ResearchAgent(orchestrator=MagicMock())
    agent.orchestrator.query_all.return_value = (
        [
            SearchResult(
                id="r1",
                title="Dummy source",
                url="https://example.com/dummy",
                snippet="RAG reduces hallucinations and allows retrieval over enterprise knowledge.",
                provider="tavily",
                query="RAG enterprise",
                relevance_score=0.9,
                normalized_url="https://example.com/dummy",
            )
        ],
        type("Run", (), {"question": "", "queries": ["RAG enterprise"], "providers_attempted": ["tavily"], "successful_providers": ["tavily"], "failed_providers": [], "raw_result_count": 1, "deduplicated_result_count": 1, "sources_selected": 1, "sources_fetched": 1, "sources_unavailable": 0, "errors": [], "provider_status": [], "model_dump": lambda self: {"good": True}})(),
    )

    monkeypatch.setattr("app.agent.fetch_document", lambda *args, **kwargs: type("Doc", (), {"id": "doc1", "title": "Dummy source", "url": "https://example.com/dummy", "provider": "tavily", "content": "Retrieval-augmented generation improves enterprise answers by grounding responses in source data.", "metadata": {}})())
    monkeypatch.setattr("app.agent.extract_evidence", lambda doc, question: [type("E", (), {"id": "e1", "source_id": "doc1", "source_url": doc.url, "source_title": doc.title, "passage": doc.content[:200], "provider": doc.provider, "relevance_reason": "direct", "question": question})()])
    monkeypatch.setattr("app.agent.synthesize_answer", lambda *args, **kwargs: type("Answer", (), {"answer": "RAG helps enterprise AI with grounded answers [doc1].", "supporting_claims": ["Grounded retrieval helps enterprise AI."], "references": [{"id": "doc1", "title": "Dummy source", "url": "https://example.com/dummy"}], "conflicts": [], "uncertainty": "Limited evidence.", "missing_evidence": ["Need more sources."], "citations": ["doc1"], "research_run": {"good": True}})())

    answer = agent.run("What is RAG?")
    assert "RAG" in answer.answer
    assert answer.references[0]["id"] == "doc1"
