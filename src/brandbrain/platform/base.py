"""Declarative base + mixins shared by every service's SQLAlchemy models.

TenantMixin enforces brand isolation at the row level: `brand_id` is non-null on every
brand-scoped table, and repositories are required to filter by it (see TDD §Trust/Isolation).
"""
from __future__ import annotations

import datetime as dt

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class TenantMixin:
    """Brand-scoping. Every brand-owned row carries an immutable brand_id."""
    brand_id: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
