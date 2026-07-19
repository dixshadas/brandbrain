from __future__ import annotations

from brandbrain.platform.auth import Principal

from .schemas import Notification, PulseDigest


class NotificationEngineImpl:
    """Fan-out consumer: turns domain events into deep-linked notifications and rolls the week up
    into the Brand Pulse. Idempotent per (event_id, recipient). See TDD §Notification Engine.
    """

    async def list_inbox(self, brand_id, principal: Principal) -> list[Notification]:  # pragma: no cover
        principal.assert_brand(brand_id)
        raise NotImplementedError

    async def mark_read(self, notification_id, principal: Principal) -> Notification:  # pragma: no cover
        raise NotImplementedError

    async def build_pulse(self, brand_id, principal: Principal) -> PulseDigest:  # pragma: no cover
        raise NotImplementedError
