from __future__ import annotations

import re


def validate_citations(answer: str, valid_ids: list[str]) -> bool:
    """Ensure citations refer only to actual retrieved source IDs."""
    citation_pattern = r"\[(S\d+|[A-Z0-9-]+)\]"
    matches = re.findall(citation_pattern, answer)
    valid = set(valid_ids)
    return all(match in valid for match in matches)
