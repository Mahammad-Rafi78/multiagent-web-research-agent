from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class ResearchQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str
    context: str = ""


class SearchQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str
    intent: str = "research"
    category: str = "general"


class SearchResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    url: str
    snippet: str = ""
    provider: str
    query: str
    published_date: str | None = None
    relevance_score: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    source_type: str = "unknown"
    normalized_url: str | None = None
    discovered_by: list[str] = Field(default_factory=list)


class SourceDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    url: str
    provider: str
    content: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class Evidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    source_id: str
    source_url: str
    source_title: str
    passage: str
    relevance_reason: str
    provider: str
    question: str


class Claim(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    text: str
    category: str = "factual"
    status: Literal["supported", "partially_supported", "conflicting", "unsupported", "insufficient_evidence"] = "unsupported"


class VerificationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    claim_id: str
    status: Literal["supported", "partially_supported", "conflicting", "unsupported", "insufficient_evidence"]
    evidence_ids: list[str] = Field(default_factory=list)
    notes: str = ""


class Conflict(BaseModel):
    model_config = ConfigDict(extra="forbid")

    claim: str
    supporting_sources: list[str] = Field(default_factory=list)
    contradicting_sources: list[str] = Field(default_factory=list)
    details: str = ""
    source_quality: str = "unknown"


class ResearchAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    answer: str
    supporting_claims: list[str] = Field(default_factory=list)
    references: list[dict[str, str]] = Field(default_factory=list)
    conflicts: list[Conflict] = Field(default_factory=list)
    uncertainty: str = ""
    missing_evidence: list[str] = Field(default_factory=list)
    citations: list[str] = Field(default_factory=list)
    research_run: dict[str, Any] | None = None


class ProviderStatus(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: str
    status: str
    attempts: int = 0
    error: str | None = None
    results: int = 0


class ResearchRun(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str
    queries: list[str] = Field(default_factory=list)
    providers_attempted: list[str] = Field(default_factory=list)
    successful_providers: list[str] = Field(default_factory=list)
    failed_providers: list[str] = Field(default_factory=list)
    raw_result_count: int = 0
    deduplicated_result_count: int = 0
    sources_selected: int = 0
    sources_fetched: int = 0
    sources_unavailable: int = 0
    errors: list[str] = Field(default_factory=list)
    provider_status: list[ProviderStatus] = Field(default_factory=list)
