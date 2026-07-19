from __future__ import annotations

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from brandbrain.platform.base import Base, TenantMixin, TimestampMixin


class RecommendedActionRow(Base, TimestampMixin, TenantMixin):
    __tablename__ = "recommended_action"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    run_id: Mapped[str] = mapped_column(String(40), index=True)
    action: Mapped[str] = mapped_column(Text)
    rationale: Mapped[str] = mapped_column(Text)
    citations_json: Mapped[list] = mapped_column(JSON, default=list)
    confidence_json: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(16), default="drafted")
