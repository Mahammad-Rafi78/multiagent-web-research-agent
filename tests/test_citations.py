from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.citations import validate_citations


def test_validate_citations_valid() -> None:
    assert validate_citations("RAG helps [S1].", ["S1"]) is True


def test_validate_citations_invalid() -> None:
    assert validate_citations("RAG helps [S9].", ["S1"]) is False
