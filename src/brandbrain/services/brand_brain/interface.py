from __future__ import annotations

from typing import Protocol

from brandbrain.platform.auth import Principal

from .schemas import BrainPage, ProposeUpdate, PublishDecision, UpdateProposal


class BrandBrainService(Protocol):
    async def get_page(self, page_id: str, principal: Principal) -> BrainPage:
        """Return the PUBLISHED page. This is the only layer agents may read."""
        ...

    async def list_pages(self, brand_id: str, principal: Principal) -> list[BrainPage]: ...

    async def propose_update(self, req: ProposeUpdate, principal: Principal) -> UpdateProposal:
        """Create a draft proposal, run machine checks (MLR), enqueue for review."""
        ...

    async def list_review_queue(self, brand_id: str, principal: Principal) -> list[UpdateProposal]: ...

    async def decide(self, proposal_id: str, decision: PublishDecision, principal: Principal) -> UpdateProposal:
        """The publish gate. REVIEWER role only. Publishing blocked if any machine check failed."""
        ...
