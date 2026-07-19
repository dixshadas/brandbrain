"""The canonical Event envelope and the catalog of domain events (the asynchronous API).

Every event is versioned (`type` includes a vN suffix) and carries brand_id + actor + trace_id,
so the event log doubles as an audit substrate. Payloads are thin: IDs and just enough context to
act, never whole documents. JSON-Schemas for these payloads are published under /contracts/events
and enforced in CI so producers and consumers can evolve independently.
"""
from __future__ import annotations

import datetime as dt
from typing import Any, Literal

from pydantic import BaseModel, Field

from brandbrain.domain.common import Actor, utcnow
from brandbrain.platform.ids import new_id


class Event(BaseModel):
    """Immutable envelope. `type` is 'noun.verb.vN'."""
    id: str = Field(default_factory=lambda: new_id("evt"))
    type: str
    occurred_at: dt.datetime = Field(default_factory=utcnow)
    brand_id: str
    actor: Actor
    trace_id: str | None = None
    idempotency_key: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)


# --------------------------------------------------------------------------- event type constants
class EventType:
    # ingestion
    DOCUMENT_RECEIVED = "document.received.v1"
    DOCUMENT_METADATA_PROPOSED = "document.metadata_proposed.v1"
    DOCUMENT_APPROVED = "document.approved.v1"           # human passed the metadata gate
    DOCUMENT_INGESTED = "document.ingested.v1"           # parsed into evidence units
    DOCUMENT_INDEXED = "document.indexed.v1"             # searchable (embeddings written)
    # synthesis
    SYNTHESIS_REQUESTED = "synthesis.requested.v1"
    SYNTHESIS_COMPLETED = "synthesis.completed.v1"
    SYNTHESIS_FAILED = "synthesis.failed.v1"
    # brand brain
    BRAIN_UPDATE_PROPOSED = "brain.update_proposed.v1"
    BRAIN_UPDATE_PUBLISHED = "brain.update_published.v1"
    BRAIN_UPDATE_REJECTED = "brain.update_rejected.v1"
    # mlr / trust
    MLR_CHECK_FAILED = "mlr.check_failed.v1"
    LOCKED_CLAIM_REGISTERED = "mlr.locked_claim_registered.v1"
    # recommendation
    RECOMMENDATION_DRAFTED = "recommendation.drafted.v1"
    # notification (usually a consumer, but re-emits for delivery receipts)
    NOTIFICATION_SENT = "notification.sent.v1"


# --------------------------------------------------------------------------- payload schemas (typed)
class DocumentReceived(BaseModel):
    document_id: str
    source: Literal["upload", "sharepoint", "sftp", "email"]
    object_key: str
    filename: str
    sha256: str


class DocumentIngested(BaseModel):
    document_id: str
    study_type: str
    evidence_unit_count: int


class DocumentIndexed(BaseModel):
    document_id: str
    indexed_units: int


class SynthesisRequested(BaseModel):
    run_id: str
    workflow: str
    source_ids: list[str]
    question: str | None = None


class SynthesisCompleted(BaseModel):
    run_id: str
    workflow: str
    finding_count: int
    contradiction_count: int
    gap_count: int
    overall_confidence: str


class BrainUpdateProposed(BaseModel):
    proposal_id: str
    page_id: str
    origin: Literal["synthesis", "ingest", "enrich", "pulse"]


class BrainUpdatePublished(BaseModel):
    proposal_id: str
    page_id: str
    version: int
    reviewer: str


class MlrCheckFailed(BaseModel):
    proposal_id: str
    check: str
    detail: str


def make_event(type_: str, *, brand_id: str, actor: Actor, payload: BaseModel, trace_id: str | None = None,
               idempotency_key: str | None = None) -> Event:
    """Helper: build a validated Event from a typed payload model."""
    return Event(
        type=type_, brand_id=brand_id, actor=actor, trace_id=trace_id,
        idempotency_key=idempotency_key, payload=payload.model_dump(mode="json"),
    )
