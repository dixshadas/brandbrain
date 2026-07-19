from __future__ import annotations

from sqlalchemy import JSON, Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from brandbrain.platform.base import Base, TenantMixin, TimestampMixin


class BrainPageRow(Base, TimestampMixin, TenantMixin):
    __tablename__ = "brain_page"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    section: Mapped[str] = mapped_column(String(64))
    title: Mapped[str] = mapped_column(String(256))
    version: Mapped[int] = mapped_column(Integer, default=1)
    facts_json: Mapped[list] = mapped_column(JSON, default=list)
    open_question: Mapped[str | None] = mapped_column(String, nullable=True)
    thin: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(16), default="published")


class BrainPageVersionRow(Base, TimestampMixin, TenantMixin):
    """Every published version is retained — the Brain is append-only history, not last-write-wins."""
    __tablename__ = "brain_page_version"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    page_id: Mapped[str] = mapped_column(String(40), index=True)
    version: Mapped[int] = mapped_column(Integer)
    facts_json: Mapped[list] = mapped_column(JSON, default=list)
    reviewer: Mapped[str | None] = mapped_column(String(128), nullable=True)


class UpdateProposalRow(Base, TimestampMixin, TenantMixin):
    __tablename__ = "brain_update_proposal"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    page_id: Mapped[str] = mapped_column(String(40), index=True)
    origin: Mapped[str] = mapped_column(String(16))
    diff_json: Mapped[list] = mapped_column(JSON, default=list)
    source_tags: Mapped[list] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(16), default="pending")
    machine_checks_json: Mapped[list] = mapped_column(JSON, default=list)
