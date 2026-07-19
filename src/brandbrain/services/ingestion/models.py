from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from brandbrain.platform.base import Base, TenantMixin, TimestampMixin


class IngestJobRow(Base, TimestampMixin, TenantMixin):
    __tablename__ = "ingest_job"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    document_id: Mapped[str] = mapped_column(String(40), index=True)
    source: Mapped[str] = mapped_column(String(20))
    filename: Mapped[str] = mapped_column(String(512))
    object_key: Mapped[str] = mapped_column(String(512))
    sha256: Mapped[str] = mapped_column(String(64), index=True)  # dedupe by content
    status: Mapped[str] = mapped_column(String(24), default="received")
    proposed_json: Mapped[str | None] = mapped_column(String, nullable=True)
    evidence_unit_count: Mapped[int] = mapped_column(Integer, default=0)
