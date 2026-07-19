from __future__ import annotations

from pydantic import BaseModel, Field


class LockedClaim(BaseModel):
    """An MLR-approved claim reproduced verbatim. Enrichment can never edit this text."""
    id: str
    brand_id: str
    mlr_ref: str                       # e.g. "BB-0142"
    text: str
    source_document_id: str
    expires_at: str | None = None


class RegisterLockedClaim(BaseModel):
    brand_id: str
    mlr_ref: str
    text: str
    source_document_id: str


class CheckRequest(BaseModel):
    """Run the guards against a proposed text change to a page/output."""
    brand_id: str
    page_id: str | None = None
    before_text: str
    after_text: str
    before_citations: list[str] = Field(default_factory=list)  # evidence_unit_ids
    after_citations: list[str] = Field(default_factory=list)


class CheckResult(BaseModel):
    name: str
    passed: bool
    detail: str


class CheckResponse(BaseModel):
    passed: bool
    results: list[CheckResult]
