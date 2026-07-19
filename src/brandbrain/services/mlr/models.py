from __future__ import annotations

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from brandbrain.platform.base import Base, TenantMixin, TimestampMixin


class LockedClaimRow(Base, TimestampMixin, TenantMixin):
    __tablename__ = "locked_claim"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    mlr_ref: Mapped[str] = mapped_column(String(32), index=True)
    text: Mapped[str] = mapped_column(Text)
    source_document_id: Mapped[str] = mapped_column(String(40))
    expires_at: Mapped[str | None] = mapped_column(String(32), nullable=True)
