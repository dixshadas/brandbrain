from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field

from brandbrain.domain.common import Citation, Confidence


class RecStatus(StrEnum):
    DRAFTED = "drafted"
    ACCEPTED = "accepted"
    DISMISSED = "dismissed"


class RecommendedAction(BaseModel):
    """Always labeled AI-drafted; always tied to the synthesis run and evidence that support it.
    The product never executes a recommendation — a human accepts or dismisses it.
    """
    id: str
    brand_id: str
    run_id: str
    action: str
    rationale: str
    supporting_citations: list[Citation] = Field(default_factory=list)
    confidence: Confidence
    status: RecStatus = RecStatus.DRAFTED


class DecideRequest(BaseModel):
    accept: bool
    note: str | None = None
