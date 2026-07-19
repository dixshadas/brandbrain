from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from brandbrain.platform.base import Base, TenantMixin, TimestampMixin


class DocumentRow(Base, TimestampMixin, TenantMixin):
    __tablename__ = "document"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    name: Mapped[str] = mapped_column(String(512))
    study_type: Mapped[str] = mapped_column(String(24))
    supplier: Mapped[str] = mapped_column(String(128))
    market: Mapped[str] = mapped_column(String(64))
    wave_or_date: Mapped[str] = mapped_column(String(64))
    sha256: Mapped[str] = mapped_column(String(64), index=True)
    object_key: Mapped[str] = mapped_column(String(512))
    page_count: Mapped[int | None] = mapped_column(Integer, nullable=True)


class EvidenceUnitRow(Base, TimestampMixin, TenantMixin):
    __tablename__ = "evidence_unit"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    document_id: Mapped[str] = mapped_column(String(40), ForeignKey("document.id"), index=True)
    locator_type: Mapped[str] = mapped_column(String(16))
    locator_value: Mapped[str] = mapped_column(String(64))
    text: Mapped[str] = mapped_column(Text)
    # embedding lives in pgvector; for the pgvector adapter this is a Vector column instead.
    embedding_ref: Mapped[str | None] = mapped_column(String(64), nullable=True)
