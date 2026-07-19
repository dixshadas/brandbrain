from __future__ import annotations

from sqlalchemy import JSON, BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from brandbrain.platform.base import Base, TimestampMixin


class AuditRecordRow(Base, TimestampMixin):
    """No TenantMixin override needed beyond brand_id; audit is written by every service.
    Rows are INSERT-only; there is deliberately no update/delete path in the repository.
    """
    __tablename__ = "audit_record"
    seq: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    id: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    brand_id: Mapped[str] = mapped_column(String(40), index=True)
    action: Mapped[str] = mapped_column(String(64), index=True)
    actor_json: Mapped[dict] = mapped_column(JSON)
    target_type: Mapped[str] = mapped_column(String(48))
    target_id: Mapped[str] = mapped_column(String(40), index=True)
    detail_json: Mapped[dict] = mapped_column(JSON, default=dict)
    prev_hash: Mapped[str] = mapped_column(String(64))
    hash: Mapped[str] = mapped_column(String(64))
