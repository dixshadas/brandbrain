from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field

from brandbrain.domain.common import Citation, ReviewStatus


class Origin(StrEnum):
    SYNTHESIS = "synthesis"
    INGEST = "ingest"
    ENRICH = "enrich"
    PULSE = "pulse"


class BrainFact(BaseModel):
    statement: str
    citations: list[Citation] = Field(default_factory=list)
    locked: bool = Field(default=False, description="MLR-locked; reproduced verbatim, never edited")


class BrainPage(BaseModel):
    id: str
    brand_id: str
    section: str
    title: str
    version: int
    facts: list[BrainFact]
    open_question: str | None = None
    thin: bool = Field(default=False, description="flagged low-evidence area, not padded with inference")
    reviewed_by: str | None = None
    reviewed_at: str | None = None


class DiffLine(BaseModel):
    op: str                # "add" | "remove"
    text: str


class UpdateProposal(BaseModel):
    """A draft change awaiting the review gate. Agents read only PUBLISHED pages, never proposals."""
    id: str
    brand_id: str
    page_id: str
    origin: Origin
    diff: list[DiffLine]
    source_tags: list[str] = Field(default_factory=list)
    status: ReviewStatus = ReviewStatus.PENDING
    machine_checks: list["MachineCheck"] = Field(default_factory=list)


class MachineCheck(BaseModel):
    name: str              # "locked_claim_guard" | "citation_preservation" | "change_summary"
    passed: bool
    detail: str


class ProposeUpdate(BaseModel):
    page_id: str
    origin: Origin
    diff: list[DiffLine]
    source_tags: list[str] = Field(default_factory=list)


class PublishDecision(BaseModel):
    approve: bool
    note: str | None = None


UpdateProposal.model_rebuild()
