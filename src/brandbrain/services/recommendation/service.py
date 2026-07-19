from __future__ import annotations

from brandbrain.platform.auth import Principal, Role

from .schemas import DecideRequest, RecommendedAction


class RecommendationEngineImpl:
    """Drafts a recommended action from a completed synthesis (RECOMMENDATION-layer Finding),
    then waits for a human. See TDD §Recommendation Engine — deliberately not an agent.
    """

    async def list_for_run(self, run_id, principal: Principal) -> list[RecommendedAction]:  # pragma: no cover
        raise NotImplementedError

    async def decide(self, rec_id, decision: DecideRequest, principal: Principal) -> RecommendedAction:  # pragma: no cover
        principal.require_role(Role.ANALYST, Role.REVIEWER)
        raise NotImplementedError
