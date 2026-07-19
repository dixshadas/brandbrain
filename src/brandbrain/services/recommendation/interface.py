from __future__ import annotations

from typing import Protocol

from brandbrain.platform.auth import Principal

from .schemas import DecideRequest, RecommendedAction


class RecommendationEngine(Protocol):
    async def list_for_run(self, run_id: str, principal: Principal) -> list[RecommendedAction]: ...
    async def decide(self, rec_id: str, decision: DecideRequest, principal: Principal) -> RecommendedAction:
        """Human accept/dismiss. This is the only state transition; nothing is auto-actioned."""
        ...
