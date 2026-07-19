from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field

from brandbrain.domain.common import StudyType


class IngestSource(StrEnum):
    UPLOAD = "upload"
    SHAREPOINT = "sharepoint"
    SFTP = "sftp"
    EMAIL = "email"


class ProposedMetadata(BaseModel):
    """AI-detected metadata. Every field is a proposal until a human confirms it."""
    brand_id: str | None = None
    study_type: StudyType | None = None
    supplier: str | None = None
    market: str | None = None
    wave_or_date: str | None = None
    confidence: float = Field(ge=0, le=1, default=0.0)


class StartIngestRequest(BaseModel):
    source: IngestSource
    filename: str
    content_type: str
    size_bytes: int
    # For uploads the bytes arrive via multipart; connectors pass an object_key instead.
    object_key: str | None = None


class IngestJob(BaseModel):
    job_id: str
    document_id: str
    source: IngestSource
    filename: str
    status: str                       # received | parsing | needs_review | indexing | ready | failed
    proposed: ProposedMetadata | None = None


class ConfirmMetadataRequest(BaseModel):
    """The human review gate. The reviewer confirms/overrides; nothing indexes before this."""
    brand_id: str
    study_type: StudyType
    supplier: str
    market: str
    wave_or_date: str
