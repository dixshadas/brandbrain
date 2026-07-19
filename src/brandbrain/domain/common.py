"""Shared value objects. These types are the product's trust guarantees expressed as code.

If it isn't representable here, it can't appear in an output — e.g. there is no way to state a
finding without attaching Citations, and no way to express certainty without a ConfidenceBand and
a rationale. The type system is the first line of the trust architecture.
"""
from __future__ import annotations

import datetime as dt
from enum import StrEnum

from pydantic import BaseModel, Field, model_validator


# --------------------------------------------------------------------------- enums
class StudyType(StrEnum):
    ATU = "atu"
    QUAL = "qual"
    TRANSCRIPT = "transcript"
    AUDIO = "audio"
    DATA = "data"
    SYNDICATED = "syndicated"
    STRATEGY = "strategy"
    QUESTIONNAIRE = "questionnaire"


class Method(StrEnum):
    QUANT = "quant"
    QUAL = "qual"
    MIXED = "mixed"
    SECONDARY = "secondary"


class ClaimLayer(StrEnum):
    """The non-negotiable separation between what research says and what the AI concludes."""
    FACT = "fact"                       # what a specific source states
    INSIGHT = "insight"                 # a pattern across multiple sources
    INTERPRETATION = "interpretation"   # what the pattern may mean
    RECOMMENDATION = "recommendation"   # what the AI advises (always human-reviewed)


class ConfidenceBand(StrEnum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


class LocatorType(StrEnum):
    PAGE = "page"
    SLIDE = "slide"
    TIMECODE = "timecode"     # audio/video, e.g. "00:14:32"
    CELL = "cell"             # spreadsheet sheet!cell
    PARAGRAPH = "paragraph"


class ReviewStatus(StrEnum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    PUBLISHED = "published"
    REJECTED = "rejected"
    FLAGGED = "flagged"       # a machine check failed; publishing blocked


class RunStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# --------------------------------------------------------------------------- value objects
class SourceLocator(BaseModel):
    """The atomic 'where' of a citation. Exactly one locator per cited span."""
    type: LocatorType
    value: str = Field(description="e.g. '12' for a slide/page, '00:14:32' for timecode, 'Topline!B4'")

    def human(self) -> str:
        pretty = {LocatorType.PAGE: "p.", LocatorType.SLIDE: "slide ", LocatorType.TIMECODE: "@",
                  LocatorType.CELL: "", LocatorType.PARAGRAPH: "¶"}
        return f"{pretty[self.type]}{self.value}"


class Citation(BaseModel):
    """A verifiable pointer into the Evidence Store. Rendered as a click-to-source chip."""
    evidence_unit_id: str
    document_id: str
    document_name: str
    locator: SourceLocator
    quote: str | None = Field(default=None, description="verbatim span; distinguishes quote from paraphrase")
    is_verbatim: bool = False


class ConfidenceRationale(BaseModel):
    """Why the confidence is what it is — the explainability requirement, never a bare number."""
    evidence_count: int
    source_quality: float = Field(ge=0, le=1)
    recency_score: float = Field(ge=0, le=1)
    method_triangulation: bool = Field(description="do quant and qual agree?")
    consistency: float = Field(ge=0, le=1, description="1 - contradiction density")
    notes: str = ""


class Confidence(BaseModel):
    band: ConfidenceBand
    score: float = Field(ge=0, le=1, description="continuous; band is derived, capped by rationale")
    rationale: ConfidenceRationale

    @model_validator(mode="after")
    def _cap(self) -> "Confidence":
        # Honesty rule: a single source can never read as HIGH confidence.
        if self.rationale.evidence_count <= 1 and self.band == ConfidenceBand.HIGH:
            raise ValueError("HIGH confidence requires more than one supporting source")
        return self


class Finding(BaseModel):
    """A single claim in an output, tagged by layer and never without citations (unless a gap)."""
    layer: ClaimLayer
    statement: str
    citations: list[Citation] = Field(default_factory=list)
    confidence: Confidence | None = None

    @model_validator(mode="after")
    def _facts_need_citations(self) -> "Finding":
        if self.layer in (ClaimLayer.FACT, ClaimLayer.INSIGHT) and not self.citations:
            raise ValueError(f"{self.layer} findings must carry at least one citation")
        return self


class Contradiction(BaseModel):
    """A mixed signal, preserved — never averaged. Both sides keep their own sources."""
    topic: str
    side_a: Finding
    side_b: Finding
    why_it_matters: str
    method_a: Method
    method_b: Method


class EvidenceGap(BaseModel):
    """What the evidence cannot answer. Turns silence into a drafted next-study question."""
    description: str
    severity: ConfidenceBand = ConfidenceBand.MODERATE
    drafted_question: str | None = None


class BrandRef(BaseModel):
    brand_id: str
    name: str


class Actor(BaseModel):
    """Who (or what) took an action — stamped on every audit record and event."""
    subject: str
    display_name: str
    kind: str = Field(default="user", description="user | service | agent")


class Money(BaseModel):
    amount: float
    currency: str = "USD"


def utcnow() -> dt.datetime:
    return dt.datetime.now(dt.UTC)
