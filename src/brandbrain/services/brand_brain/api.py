from __future__ import annotations

from fastapi import APIRouter, Depends

from brandbrain.platform.auth import Principal, Role, get_principal

from .interface import BrandBrainService
from .schemas import BrainPage, ProposeUpdate, PublishDecision, UpdateProposal
from .service import BrandBrainServiceImpl

router = APIRouter(prefix="/v1/brain", tags=["Brand Brain"])


def get_service() -> BrandBrainService:
    return BrandBrainServiceImpl()


@router.get("/pages", response_model=list[BrainPage], summary="List published brain pages")
async def list_pages(brand_id: str, principal: Principal = Depends(get_principal),
                     svc: BrandBrainService = Depends(get_service)) -> list[BrainPage]:
    return await svc.list_pages(brand_id, principal)


@router.get("/pages/{page_id}", response_model=BrainPage, summary="Get a published page (agent-readable layer)")
async def get_page(page_id: str, principal: Principal = Depends(get_principal),
                   svc: BrandBrainService = Depends(get_service)) -> BrainPage:
    return await svc.get_page(page_id, principal)


@router.post("/proposals", response_model=UpdateProposal, status_code=201, summary="Propose a page update")
async def propose(req: ProposeUpdate, principal: Principal = Depends(get_principal),
                  svc: BrandBrainService = Depends(get_service)) -> UpdateProposal:
    principal.require_role(Role.ANALYST, Role.REVIEWER)
    return await svc.propose_update(req, principal)


@router.get("/review-queue", response_model=list[UpdateProposal], summary="Pending proposals")
async def review_queue(brand_id: str, principal: Principal = Depends(get_principal),
                       svc: BrandBrainService = Depends(get_service)) -> list[UpdateProposal]:
    return await svc.list_review_queue(brand_id, principal)


@router.post("/proposals/{proposal_id}/decision", response_model=UpdateProposal,
             summary="Approve & publish or reject (governance gate)")
async def decide(proposal_id: str, decision: PublishDecision, principal: Principal = Depends(get_principal),
                 svc: BrandBrainService = Depends(get_service)) -> UpdateProposal:
    principal.require_role(Role.REVIEWER)
    return await svc.decide(proposal_id, decision, principal)
