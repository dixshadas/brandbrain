from __future__ import annotations

from fastapi import APIRouter, Depends

from brandbrain.platform.auth import Principal, get_principal

from .interface import RecommendationEngine
from .schemas import DecideRequest, RecommendedAction
from .service import RecommendationEngineImpl

router = APIRouter(prefix="/v1/recommendations", tags=["Recommendation Engine"])


def get_service() -> RecommendationEngine:
    return RecommendationEngineImpl()


@router.get("/runs/{run_id}", response_model=list[RecommendedAction], summary="Recommendations for a run")
async def list_for_run(run_id: str, principal: Principal = Depends(get_principal),
                       svc: RecommendationEngine = Depends(get_service)) -> list[RecommendedAction]:
    return await svc.list_for_run(run_id, principal)


@router.post("/{rec_id}/decision", response_model=RecommendedAction, summary="Accept or dismiss (human only)")
async def decide(rec_id: str, decision: DecideRequest, principal: Principal = Depends(get_principal),
                 svc: RecommendationEngine = Depends(get_service)) -> RecommendedAction:
    return await svc.decide(rec_id, decision, principal)
