from __future__ import annotations

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from brandbrain.platform.base import Base, TenantMixin, TimestampMixin


class SynthesisRunRow(Base, TimestampMixin, TenantMixin):
    __tablename__ = "synthesis_run"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    workflow: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(16), default="queued")
    question: Mapped[str | None] = mapped_column(String, nullable=True)
    source_ids: Mapped[list] = mapped_column(JSON, default=list)
    output_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    llm_call_ids: Mapped[list] = mapped_column(JSON, default=list)
