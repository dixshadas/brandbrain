from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class Channel(StrEnum):
    IN_APP = "in_app"
    EMAIL = "email"
    SLACK = "slack"
    TEAMS = "teams"


class Notification(BaseModel):
    id: str
    brand_id: str
    kind: str                          # "review_pending" | "wave_indexed" | "pulse_ready" | "signal"
    title: str
    body: str
    deep_link: str                     # routes into the exact flow (e.g. /brain/review-queue?id=...)
    channels: list[Channel] = Field(default_factory=lambda: [Channel.IN_APP])
    read: bool = False


class PulseDigest(BaseModel):
    """The weekly Brand Pulse: what changed, why it matters, what needs review."""
    brand_id: str
    week_of: str
    items: list[Notification]
