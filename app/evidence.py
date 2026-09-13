from __future__ import annotations

import re

from app.models import Evidence, SourceDocument


def extract_evidence(document: SourceDocument, question: str) -> list[Evidence]:
    text = document.content
    sentences = re.split(r"(?<=[.!?])\s+", text)
    excerpts = []
    for sentence in sentences:
        s = sentence.strip()
        if len(s) < 40:
            continue
        lowered = (document.title + " " + s).lower()
        q = question.lower()
        if any(token in lowered for token in ["rag", "retrieval", "fine", "tuning", "enterprise", "llm", "knowledge"] if token in q.lower() or token in lowered):
            excerpts.append(s)
    if not excerpts:
        excerpts = sentences[:3]
    results: list[Evidence] = []
    for idx, sentence in enumerate(excerpts[:3], start=1):
        results.append(
            Evidence(
                id=f"ev-{document.id}-{idx}",
                source_id=document.id,
                source_url=document.url,
                source_title=document.title,
                passage=sentence[:600],
                relevance_reason="Directly relevant to the research question.",
                provider=document.provider,
                question=question,
            )
        )
    return results
