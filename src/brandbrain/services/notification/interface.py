from __future__ import annotations

from typing import Protocol

from brandbrain.platform.auth import Principal

from .schemas import Notification, PulseDigest


class NotificationEngine(Protocol):
    async def list_inbox(self, brand_id: str, principal: Principal) -> list[Notification]: ...
    async def mark_read(self, notification_id: str, principal: Principal) -> Notification: ...
    async def build_pulse(self, brand_id: str, principal: Principal) -> PulseDigest:
        """Assemble the weekly digest from the week's events (indexing, proposals, signals)."""
        ...
