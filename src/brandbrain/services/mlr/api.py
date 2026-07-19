from __future__ import annotations

from fastapi import APIRouter, Depends

from brandbrain.platform.auth import Principal, Role, get_principal

from .interface import MlrEngine
from .schemas import CheckRequest, CheckResponse, LockedClaim, RegisterLockedClaim
from .service import MlrEngineImpl

router = APIRouter(prefix="/v1/mlr", tags=["MLR Engine"])


def get_service() -> MlrEngine:
    return MlrEngineImpl()


@router.get("/locked-claims", response_model=list[LockedClaim], summary="List locked claims")
async def list_claims(brand_id: str, principal: Principal = Depends(get_principal),
                      svc: MlrEngine = Depends(get_service)) -> list[LockedClaim]:
    return await svc.list_locked_claims(brand_id, principal)


@router.post("/locked-claims", response_model=LockedClaim, status_code=201, summary="Register a locked claim")
async def register(req: RegisterLockedClaim, principal: Principal = Depends(get_principal),
                   svc: MlrEngine = Depends(get_service)) -> LockedClaim:
    principal.require_role(Role.MLR)
    return await svc.register_locked_claim(req, principal)


@router.post("/check", response_model=CheckResponse, summary="Run locked-claim + citation-preservation guards")
async def check(req: CheckRequest, principal: Principal = Depends(get_principal),
                svc: MlrEngine = Depends(get_service)) -> CheckResponse:
    return await svc.check(req, principal)
