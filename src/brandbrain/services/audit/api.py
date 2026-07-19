from __future__ import annotations

from fastapi import APIRouter, Depends

from brandbrain.platform.auth import Principal, Role, get_principal

from .interface import AuditEngine
from .schemas import AuditRecord, VerifyResponse
from .service import AuditEngineImpl

router = APIRouter(prefix="/v1/audit", tags=["Audit Engine"])


def get_service() -> AuditEngine:
    return AuditEngineImpl()


@router.get("/targets/{target_id}", response_model=list[AuditRecord], summary="Audit trail for an object")
async def for_target(target_id: str, principal: Principal = Depends(get_principal),
                     svc: AuditEngine = Depends(get_service)) -> list[AuditRecord]:
    return await svc.list_for_target(target_id, principal)


@router.get("/verify", response_model=VerifyResponse, summary="Verify the hash chain is intact")
async def verify(brand_id: str, principal: Principal = Depends(get_principal),
                 svc: AuditEngine = Depends(get_service)) -> VerifyResponse:
    principal.require_role(Role.ADMIN, Role.REVIEWER)
    return await svc.verify_chain(brand_id, principal)
