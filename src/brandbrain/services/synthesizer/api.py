from __future__ import annotations

from fastapi import APIRouter, Depends

from brandbrain.platform.auth import Principal, Role, get_principal

from .interface import SynthesizerService
from .schemas import RunRequest, SynthesisRun
from .service import SynthesizerServiceImpl

router = APIRouter(prefix="/v1/synthesis", tags=["Cross-Study Synthesizer"])


def get_service() -> SynthesizerService:
    return SynthesizerServiceImpl()


@router.post("/runs", response_model=SynthesisRun, status_code=202,
             summary="Request a synthesis run (async; confirm scope first)")
async def request_run(req: RunRequest, principal: Principal = Depends(get_principal),
                      svc: SynthesizerService = Depends(get_service)) -> SynthesisRun:
    principal.require_role(Role.ANALYST, Role.REVIEWER)
    return await svc.request_run(req, principal)


@router.get("/runs/{run_id}", response_model=SynthesisRun, summary="Get a synthesis run + output")
async def get_run(run_id: str, principal: Principal = Depends(get_principal),
                  svc: SynthesizerService = Depends(get_service)) -> SynthesisRun:
    return await svc.get_run(run_id, principal)
