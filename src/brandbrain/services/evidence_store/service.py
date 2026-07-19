from __future__ import annotations

from brandbrain.platform.auth import Principal

from .schemas import AddEvidenceUnits, Document, EvidenceUnit, RegisterDocument


class EvidenceStoreImpl:
    """Documents + evidence units are append-only; corrections are new versions, never mutations,
    so a citation captured last quarter still resolves to the same bytes. See TDD §Evidence Store.
    """

    async def register_document(self, req: RegisterDocument, principal: Principal) -> Document:  # pragma: no cover
        principal.assert_brand(req.brand_id)
        raise NotImplementedError

    async def get_document(self, document_id, principal: Principal) -> Document:  # pragma: no cover
        raise NotImplementedError

    async def add_evidence_units(self, req: AddEvidenceUnits, principal: Principal) -> int:  # pragma: no cover
        raise NotImplementedError

    async def get_evidence_unit(self, unit_id, principal: Principal) -> EvidenceUnit:  # pragma: no cover
        raise NotImplementedError

    async def list_documents(self, brand_id, principal: Principal) -> list[Document]:  # pragma: no cover
        principal.assert_brand(brand_id)
        raise NotImplementedError
