from __future__ import annotations

from pydantic import BaseModel, Field

from brandbrain.domain.common import SourceLocator, StudyType


class Document(BaseModel):
    id: str
    brand_id: str
    name: str
    study_type: StudyType
    supplier: str
    market: str
    wave_or_date: str
    sha256: str
    object_key: str
    page_count: int | None = None


class EvidenceUnit(BaseModel):
    """The atom of the system: a citable span (a slide, a page, a transcript turn, a table cell).

    Everything downstream cites an EvidenceUnit by id, so a citation is always re-verifiable.
    """
    id: str
    brand_id: str
    document_id: str
    locator: SourceLocator
    text: str
    embedding_ref: str | None = Field(default=None, description="vector store handle")


class RegisterDocument(BaseModel):
    brand_id: str
    name: str
    study_type: StudyType
    supplier: str
    market: str
    wave_or_date: str
    sha256: str
    object_key: str


class AddEvidenceUnits(BaseModel):
    document_id: str
    units: list[EvidenceUnit]
