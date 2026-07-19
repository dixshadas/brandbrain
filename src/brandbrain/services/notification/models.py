from __future__ import annotations

from sqlalchemy import JSON, Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from brandbrain.platform.base import Base, TenantMixin, TimestampMixin


class NotificationRow(Base, TimestampMixin, TenantMixin):
    __tablename__ = "notification"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    kind: Mapped[str] = mapped_column(String(32), index=True)
    title: Mapped[str] = mapped_column(String(256))
    body: Mapped[str] = mapped_column(Text)
    deep_link: Mapped[str] = mapped_column(String(512))
    channels_json: Mapped[list] = mapped_column(JSON, default=list)
    read: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
