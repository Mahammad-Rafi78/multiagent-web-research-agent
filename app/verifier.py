from __future__ import annotations

from app.models import Claim, Evidence, VerificationResult


def verify_claim(claim: Claim, evidence: list[Evidence]) -> VerificationResult:
    if not evidence:
        return VerificationResult(
            claim_id=claim.id,
            status="insufficient_evidence",
            evidence_ids=[],
            notes="No direct evidence was retrieved for this claim.",
        )

    support_count = len(evidence)
    if claim.category == "conflict":
        return VerificationResult(
            claim_id=claim.id,
            status="conflicting",
            evidence_ids=[e.id for e in evidence],
            notes="Evidence points to a factual conflict between sources.",
        )

    if support_count >= 2:
        return VerificationResult(
            claim_id=claim.id,
            status="supported",
            evidence_ids=[e.id for e in evidence],
            notes="Multiple independent sources support the claim.",
        )

    return VerificationResult(
        claim_id=claim.id,
        status="partially_supported",
        evidence_ids=[e.id for e in evidence],
        notes="The claim is only partially supported by one retrieved source.",
    )
