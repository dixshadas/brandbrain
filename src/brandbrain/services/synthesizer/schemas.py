from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field

from brandbrain.domain.common import (
    Confidence,
    Contradiction,
    EvidenceGap,
    Finding,
    RunStatus,
)


class Workflow(StrEnum):
    """Named, pharma-grade frameworks — not free-form prompts. Each maps to a method + source rule."""
    BRAND_STUDY_LENS = "brand_study_lens"          # cross-study concordance (min 2 sources)
    BRAND_HEALTH = "brand_health"                  # wave-over-wave significance
    EVIDENCE_IQ = "evidence_iq"                    # message–claim support matrix
    MARKET_PULSE = "market_pulse"                  # weekly signal triage
    BRAND_PULSE = "brand_pulse"                    # brand-truth synthesis over the published Brain


class RunRequest(BaseModel):
    """A run never starts until the user confirms scope. This is that confirmed scope."""
    brand_id: str
    workflow: Workflow
    source_ids: list[str] = Field(default_factory=list, description="evidence documents / brain pages")
    question: str | None = None

    def validate_scope(self) -> None:
        if self.workflow == Workflow.BRAND_STUDY_LENS and len(self.source_ids) < 2:
            raise ValueError("Brand Study Lens needs at least two sources — mixing methods is the point.")


class MetricDelta(BaseModel):
    metric: str
    values: dict[str, str]              # e.g. {"W2": "18%", "W3": "27%", "W4": "34%"}
    delta: str                          # "+7pp"
    significant: bool
    read_from: str = Field(description="source table reference — never read off a chart")


class SynthesisOutput(BaseModel):
    """The output anatomy. Ordered for 10-second executive comprehension, drillable to the source.

    Note the deliberate separation: `story_summary` and `agreements` are grounded Findings;
    `contradictions` are preserved (never averaged); `gaps` name what we don't know; the
    recommendation is a separate, clearly-labeled RECOMMENDATION-layer Finding.
    """
    story_summary: Finding                              # leadership headline (INSIGHT layer)
    agreements: list[Finding] = Field(default_factory=list)
    contradictions: list[Contradiction] = Field(default_factory=list)
    open_questions: list[EvidenceGap] = Field(default_factory=list)
    metrics_changed: list[MetricDelta] = Field(default_factory=list)
    recommended_action: Finding | None = None           # RECOMMENDATION layer, human-review required
    overall_confidence: Confidence
    ai_generated: bool = True
    review_notice: str = "AI-drafted · review before sharing"


class SynthesisRun(BaseModel):
    run_id: str
    brand_id: str
    workflow: Workflow
    status: RunStatus
    source_ids: list[str]
    question: str | None = None
    output: SynthesisOutput | None = None
    llm_call_ids: list[str] = Field(default_factory=list, description="for reproducibility/audit")
