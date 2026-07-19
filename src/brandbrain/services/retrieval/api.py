from __future__ import annotations

from fastapi import APIRouter, Depends

from brandbrain.platform.auth import Principal, get_principal

from .interface import RetrievalService
from .schemas import SearchRequest, SearchResponse
from .service import RetrievalServiceImpl

router = APIRouter(prefix="/v1/search", tags=["Evidence Retrieval"])


def get_service() -> RetrievalService:
    return RetrievalServiceImpl()


@router.post("", response_model=SearchResponse, summary="Hybrid search across the estate")
async def search(req: SearchRequest, principal: Principal = Depends(get_principal),
                 svc: RetrievalService = Depends(get_service)) -> SearchResponse:
    return await svc.search(req, principal)
