from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.config import Settings, ensure_api_key


def test_settings_defaults() -> None:
    settings = Settings()
    assert settings.REQUEST_TIMEOUT > 0
    assert settings.MAX_RETRIES >= 1


def test_ensure_api_key() -> None:
    os.environ["OPENAI_API_KEY"] = "abc"
    settings = Settings()
    assert ensure_api_key("OPENAI_API_KEY") == "abc"
    del os.environ["OPENAI_API_KEY"]
