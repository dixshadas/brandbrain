from __future__ import annotations

from pydantic import BaseModel, Field

from brandbrain.domain.common import Actor, utcnow


class AuditRecord(BaseModel):
    """One tamper-evident entry. `prev_hash` + `hash` form a chain: altering any past record
    invalidates every record after it, so the log is verifiably intact.
    """
    id: str
    brand_id: str
    action: str                        # e.g. "brain.published", "synthesis.completed"
    actor: Actor
    target_type: str
    target_id: str
    detail: dict = Field(default_factory=dict)
    occurred_at: str = Field(default_factory=lambda: utcnow().isoformat())
    prev_hash: str
    hash: str


class AppendRecord(BaseModel):
    brand_id: str
    action: str
    actor: Actor
    target_type: str
    target_id: str
    detail: dict = Field(default_factory=dict)


class VerifyResponse(BaseModel):
    intact: bool
    checked: int
    broken_at: str | None = None
