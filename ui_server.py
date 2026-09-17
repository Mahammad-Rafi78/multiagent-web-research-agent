from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.agent import ResearchAgent

app = FastAPI(title="Multi-Source Web Research Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"


class ResearchRequest(BaseModel):
    question: str = Field(..., min_length=3)


def build_demo_result(question: str) -> dict:
    return {
        "demo_mode": True,
        "question": question,
        "answer": (
            "This is a demo result from the local research interface. The system is designed to combine evidence from multiple providers, "
            "deduplicate sources, and carefully note uncertainty before answering. In a real run, the agent would fetch and rank live evidence."
        ),
        "supporting_claims": [
            "Using two independent providers reduces dependence on a single search ecosystem.",
            "Evidence-aware synthesis is more reliable than one-shot search-to-answer chains.",
            "Conflict and uncertainty reporting improves trustworthiness."
        ],
        "references": [
            {"id": "S1", "title": "Demo evidence note", "url": "https://example.com/demo"},
            {"id": "S2", "title": "Research design overview", "url": "https://example.com/design"}
        ],
        "conflicts": [{"details": "No conflicting evidence detected in this demo run."}],
        "missing_evidence": ["Live provider data is not available in this local demo mode."],
        "research_run": {
            "queries": [question],
            "providers_attempted": ["tavily", "brave"],
            "sources_fetched": 0,
            "sources_unavailable": 0,
            "provider_status": [
                {"provider": "tavily", "status": "demo"},
                {"provider": "brave", "status": "demo"}
            ]
        },
    }


@app.get("/")
async def serve_index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/static/{filename}")
async def serve_static(filename: str) -> FileResponse:
    file_path = FRONTEND_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Static asset not found")
    return FileResponse(file_path)


@app.get("/{filename}")
async def serve_frontend_asset(filename: str) -> FileResponse:
    if filename not in {"app.js", "styles.css"}:
        raise HTTPException(status_code=404, detail="Frontend asset not found")
    return FileResponse(FRONTEND_DIR / filename)


@app.post("/api/research")
async def research(request: ResearchRequest) -> dict:
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="A question is required.")

    try:
        answer = ResearchAgent().run(question)
        return {
            "demo_mode": False,
            "question": question,
            "answer": answer.answer,
            "supporting_claims": answer.supporting_claims,
            "references": answer.references,
            "conflicts": [{"details": conflict.details} for conflict in answer.conflicts],
            "missing_evidence": answer.missing_evidence,
            "research_run": answer.research_run,
        }
    except Exception as exc:
        demo = build_demo_result(question)
        demo["error"] = str(exc)
        return demo


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "ui_server:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=False,
    )
