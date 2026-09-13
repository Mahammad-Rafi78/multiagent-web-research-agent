from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self) -> None:
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
        self.GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
        self.GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
        self.OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/auto")
        self.LLM_PROVIDER = os.getenv("LLM_PROVIDER", "auto").lower()
        self.TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
        self.BRAVE_API_KEY = os.getenv("BRAVE_API_KEY", "")
        self.REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "20"))
        self.MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
        self.MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "8"))
        self.MAX_SOURCES_TO_FETCH = int(os.getenv("MAX_SOURCES_TO_FETCH", "5"))
        self.MAX_EVIDENCE_ITEMS = int(os.getenv("MAX_EVIDENCE_ITEMS", "6"))

    @property
    def has_openai(self) -> bool:
        return bool(self.OPENAI_API_KEY)

    @property
    def has_tavily(self) -> bool:
        return bool(self.TAVILY_API_KEY)

    @property
    def has_brave(self) -> bool:
        return bool(self.BRAVE_API_KEY)

    @property
    def has_gemini(self) -> bool:
        return bool(self.GEMINI_API_KEY)

    @property
    def has_groq(self) -> bool:
        return bool(self.GROQ_API_KEY)

    @property
    def has_openrouter(self) -> bool:
        return bool(self.OPENROUTER_API_KEY)


settings = Settings()


def ensure_api_key(name: str) -> str:
    value = os.getenv(name, "")
    if not value:
        raise ValueError(f"{name} is not configured.")
    return value


ROOT_DIR = Path(__file__).resolve().parent.parent
