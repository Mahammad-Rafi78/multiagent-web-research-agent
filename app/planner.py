from __future__ import annotations

import re
from typing import Sequence

from .config import settings
from .logging_config import get_logger
from .models import ResearchQuestion, SearchQuery

logger = get_logger(__name__)


def plan_queries(question: str | ResearchQuestion, max_queries: int = 4) -> list[SearchQuery]:
    """Generate a small set of search queries from the user question."""
    if isinstance(question, ResearchQuestion):
        question = question.question

    cleaned = re.sub(r"\s+", " ", question).strip()
    if not cleaned:
        return [SearchQuery(text="research overview")]

    lowered = cleaned.lower()
    simple_terms = {"what", "who", "when", "where", "why", "how", "is", "are"}
    words = [w for w in re.findall(r"[A-Za-z0-9][A-Za-z0-9\- ]+", cleaned) if w]

    phrases = []
    if len(words) <= 9:
        phrases.append(cleaned)
        if "vs" in lowered or "versus" in lowered or "compared" in lowered:
            phrases.append(cleaned + " advantages and limitations")
            phrases.append(cleaned + " enterprise applications")
        if "advantages" in lowered or "disadvantages" in lowered:
            phrases.append(cleaned.replace("advantages", "benefits").replace("disadvantages", "limitations"))
    else:
        core = cleaned
        phrases.append(core)
        if "compar" in lowered:
            phrases.append(core + " benefits and limitations")
        phrases.append("key facts about " + core)

    expanded = []
    seen: set[str] = set()
    for p in phrases:
        q = re.sub(r"\s+", " ", p).strip()
        if q and q.lower() not in seen:
            seen.add(q.lower())
            expanded.append(SearchQuery(text=q, category="general"))

    if not expanded:
        expanded = [SearchQuery(text=cleaned)]

    if settings.has_openai:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            model = settings.OPENAI_MODEL
            response = client.responses.create(
                model=model,
                input=[
                    {
                        "role": "system",
                        "content": "You are an expert research planner. Return 2-4 short, high-signal search queries in JSON format as a list of strings. Keep them concise and non-redundant."
                    },
                    {"role": "user", "content": cleaned},
                ],
                temperature=0,
            )
            text = getattr(response, "output_text", "")
            if text:
                import json

                parsed = json.loads(text)
                if isinstance(parsed, list):
                    queries = [SearchQuery(text=str(item).strip(), category="general") for item in parsed[:max_queries] if str(item).strip()]
                    if queries:
                        logger.info("LLM query planning succeeded.")
                        return queries[:max_queries]
        except Exception as exc:  # pragma: no cover - defensive path
            logger.warning("LLM planning failed; using fallback queries: %s", exc)

    result = expanded[:max_queries]
    logger.info("Using fallback query planning with %d queries.", len(result))
    return result


def validate_query(query: SearchQuery) -> bool:
    return bool(query.text and len(query.text.strip()) >= 3)
