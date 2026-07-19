from __future__ import annotations

from fastapi import APIRouter, Depends

from brandbrain.platform.auth import Principal, get_principal

from .interface import EvidenceStore
from .schemas import Document, EvidenceUnit, RegisterDocument
from .service import EvidenceStoreImpl

router = APIRouter(prefix="/v1/evidence", tags=["Evidence Store"])


def get_service() -> EvidenceStore:
    return EvidenceStoreImpl()


@router.get("/documents", response_model=list[Document], summary="List documents in a brand estate")
async def list_documents(brand_id: str, principal: Principal = Depends(get_principal),
                         svc: EvidenceStore = Depends(get_service)) -> list[Document]:
    return await svc.list_documents(brand_id, principal)


@router.get("/documents/{document_id}", response_model=Document, summary="Get a document")
async def get_document(document_id: str, principal: Principal = Depends(get_principal),
                       svc: EvidenceStore = Depends(get_service)) -> Document:
    return await svc.get_document(document_id, principal)


@router.get("/units/{unit_id}", response_model=EvidenceUnit, summary="Resolve a citation to its source span")
async def get_unit(unit_id: str, principal: Principal = Depends(get_principal),
                   svc: EvidenceStore = Depends(get_service)) -> EvidenceUnit:
    return await svc.get_evidence_unit(unit_id, principal)
