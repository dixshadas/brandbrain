from __future__ import annotations

from fastapi import APIRouter, Depends

from brandbrain.domain.common import Confidence

from .interface import TrustEngine
from .schemas import ClassifyRequest, ClassifyResponse, ScoreRequest
from .service import TrustEngineImpl

router = APIRouter(prefix="/v1/trust", tags=["Trust Engine"])


def get_service() -> TrustEngine:
    return TrustEngineImpl()


@router.post("/score", response_model=Confidence, summary="Compute explainable, capped confidence")
async def score(req: ScoreRequest, svc: TrustEngine = Depends(get_service)) -> Confidence:
    return await svc.score(req)


@router.post("/classify", response_model=ClassifyResponse, summary="Classify a statement's claim layer")
async def classify(req: ClassifyRequest, svc: TrustEngine = Depends(get_service)) -> ClassifyResponse:
    return await svc.classify(req)
