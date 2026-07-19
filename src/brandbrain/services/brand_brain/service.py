from __future__ import annotations

from brandbrain.platform.auth import Principal, Role
from brandbrain.platform.errors import GovernanceError

from .schemas import BrainPage, ProposeUpdate, PublishDecision, UpdateProposal


class BrandBrainServiceImpl:
    """Draft-first, review-gated, brand-isolated. Publishing bumps the page version and writes an
    immutable BrainPageVersion. Any failed machine check blocks publishing (see TDD §Brand Brain).
    """

    async def get_page(self, page_id, principal: Principal) -> BrainPage:  # pragma: no cover
        raise NotImplementedError

    async def list_pages(self, brand_id, principal: Principal) -> list[BrainPage]:  # pragma: no cover
        principal.assert_brand(brand_id)
        raise NotImplementedError

    async def propose_update(self, req: ProposeUpdate, principal: Principal) -> UpdateProposal:  # pragma: no cover
        raise NotImplementedError

    async def list_review_queue(self, brand_id, principal: Principal) -> list[UpdateProposal]:  # pragma: no cover
        raise NotImplementedError

    async def decide(self, proposal_id, decision: PublishDecision, principal: Principal) -> UpdateProposal:  # pragma: no cover
        principal.require_role(Role.REVIEWER)
        if decision.approve:
            # guard: publishing is refused if any machine check failed
            raise GovernanceError("stub: verify machine_checks all passed before publish")
        raise NotImplementedError
