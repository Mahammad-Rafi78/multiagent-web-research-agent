from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ui_server import app

client = TestClient(app)


def test_frontend_served() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Research Agent" in response.text


def test_api_research_returns_json() -> None:
    response = client.post("/api/research", json={"question": "What is RAG?"})
    assert response.status_code == 200
    payload = response.json()
    assert "answer" in payload
    assert payload["question"] == "What is RAG?"
