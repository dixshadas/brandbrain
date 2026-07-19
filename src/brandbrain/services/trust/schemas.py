from __future__ import annotations

from pydantic import BaseModel, Field

from brandbrain.domain.common import ClaimLayer, Confidence, Method


class EvidenceSignal(BaseModel):
    """One piece of evidence bearing on a statement, with the metadata confidence needs."""
    evidence_unit_id: str
    supports: bool                     # supports (True) or contradicts (False) the statement
    method: Method
    source_quality: float = Field(ge=0, le=1)
    recency_score: float = Field(ge=0, le=1)


class ScoreRequest(BaseModel):
    statement: str
    signals: list[EvidenceSignal]


class ClassifyRequest(BaseModel):
    statement: str
    has_citations: bool
    crosses_sources: bool
    is_advice: bool


class ClassifyResponse(BaseModel):
    layer: ClaimLayer
    reason: str
