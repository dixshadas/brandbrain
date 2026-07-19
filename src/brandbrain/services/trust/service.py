from __future__ import annotations

from brandbrain.domain.common import (
    ClaimLayer,
    Confidence,
    ConfidenceBand,
    ConfidenceRationale,
)

from .schemas import ClassifyRequest, ClassifyResponse, ScoreRequest


class TrustEngineImpl:
    """Confidence is a deterministic function of the evidence — reproducible and explainable.
    Crucially it is *capped*: one source can never yield HIGH. See TDD §Trust Engine.
    """

    async def score(self, req: ScoreRequest) -> Confidence:
        supporting = [s for s in req.signals if s.supports]
        contradicting = [s for s in req.signals if not s.supports]
        n = len(supporting)
        quality = sum(s.source_quality for s in supporting) / n if n else 0.0
        recency = sum(s.recency_score for s in supporting) / n if n else 0.0
        methods = {s.method for s in supporting}
        triangulated = len(methods) > 1
        total = len(req.signals) or 1
        consistency = 1.0 - (len(contradicting) / total)

        raw = (0.35 * min(n, 5) / 5) + 0.2 * quality + 0.15 * recency \
            + 0.15 * (1.0 if triangulated else 0.0) + 0.15 * consistency
        if n <= 1:
            raw = min(raw, 0.5)            # honesty cap: single source -> never HIGH
        band = ConfidenceBand.HIGH if raw >= 0.75 else ConfidenceBand.MODERATE if raw >= 0.45 else ConfidenceBand.LOW

        return Confidence(
            band=band,
            score=round(raw, 3),
            rationale=ConfidenceRationale(
                evidence_count=n,
                source_quality=round(quality, 3),
                recency_score=round(recency, 3),
                method_triangulation=triangulated,
                consistency=round(consistency, 3),
                notes="capped: single-source" if n <= 1 else "",
            ),
        )

    async def classify(self, req: ClassifyRequest) -> ClassifyResponse:
        if req.is_advice:
            return ClassifyResponse(layer=ClaimLayer.RECOMMENDATION, reason="states an action to take")
        if not req.has_citations:
            return ClassifyResponse(layer=ClaimLayer.INTERPRETATION, reason="no direct source; a reading")
        if req.crosses_sources:
            return ClassifyResponse(layer=ClaimLayer.INSIGHT, reason="pattern across multiple sources")
        return ClassifyResponse(layer=ClaimLayer.FACT, reason="single sourced statement")
