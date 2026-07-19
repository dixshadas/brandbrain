from __future__ import annotations

from fastapi import APIRouter, Depends

from brandbrain.platform.auth import Principal, get_principal

from .interface import IngestionService
from .schemas import ConfirmMetadataRequest, IngestJob, StartIngestRequest
from .service import IngestionServiceImpl

router = APIRouter(prefix="/v1/ingestion", tags=["Research Ingestion"])


def get_service() -> IngestionService:
    return IngestionServiceImpl()


@router.post("/jobs", response_model=IngestJob, status_code=201, summary="Start ingesting a document")
async def start_ingest(
    req: StartIngestRequest,
    principal: Principal = Depends(get_principal),
    svc: IngestionService = Depends(get_service),
) -> IngestJob:
    return await svc.start(req, principal)


@router.get("/jobs/{job_id}", response_model=IngestJob, summary="Get ingestion job status")
async def get_job(
    job_id: str,
    principal: Principal = Depends(get_principal),
    svc: IngestionService = Depends(get_service),
) -> IngestJob:
    return await svc.get_job(job_id, principal)


@router.post("/jobs/{job_id}/confirm", response_model=IngestJob, summary="Confirm metadata (governance gate)")
async def confirm_metadata(
    job_id: str,
    req: ConfirmMetadataRequest,
    principal: Principal = Depends(get_principal),
    svc: IngestionService = Depends(get_service),
) -> IngestJob:
    return await svc.confirm_metadata(job_id, req, principal)
