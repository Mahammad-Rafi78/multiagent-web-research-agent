from __future__ import annotations

import re

from app.models import Conflict, Evidence


def _normalize_claim_terms(text: str) -> str:
    cleaned = re.sub(r"[^a-z0-9\s]", " ", text.lower())
    cleaned = re.sub(r"\b(not|no|never|does not|did not|doesn['’]t|didn['’]t)\b", " ", cleaned)
    stopwords = {"the", "a", "an", "and", "or", "but", "for", "with", "about", "that", "this", "does", "do", "did", "is", "are", "it", "of", "to", "in", "on", "we", "they", "their", "them", "our", "was", "were", "have", "has", "had"}
    words = []
    for word in cleaned.split():
        if word in stopwords:
            continue
        if word.endswith("uces"):
            word = word[:-1]
        elif word.endswith("ies") and len(word) > 4:
            word = word[:-3] + "y"
        elif word.endswith("sses"):
            word = word[:-2]
        elif word.endswith("es") and len(word) > 4:
            word = word[:-2]
        elif word.endswith("s") and len(word) > 3 and not word.endswith("ss"):
            word = word[:-1]
        words.append(word)
    return " ".join(words)


def detect_conflicts(evidence: list[Evidence]) -> list[Conflict]:
    """Detect directly contradictory evidence. This is intentionally conservative."""
    conflicts: list[Conflict] = []
    if len(evidence) < 2:
        return conflicts

    groups: dict[str, list[Evidence]] = {}
    for item in evidence:
        normalized = _normalize_claim_terms(item.passage)
        if not normalized:
            continue
        groups.setdefault(normalized, []).append(item)

    for items in groups.values():
        if len(items) < 2:
            continue
        negated_sources = []
        positive_sources = []
        for item in items:
            text = item.passage.lower()
            negated = bool(re.search(r"\b(not|no|never|does not|did not|doesn['’]t|didn['’]t)\b", text))
            if negated:
                negated_sources.append(item.source_id)
            else:
                positive_sources.append(item.source_id)
        if positive_sources and negated_sources:
            conflicts.append(
                Conflict(
                    claim="Evidence in this cluster contains opposing polarity.",
                    supporting_sources=positive_sources,
                    contradicting_sources=negated_sources,
                    details="Multiple sources express opposite conclusions in closely related passages.",
                    source_quality="mixed",
                )
            )
    return conflicts
