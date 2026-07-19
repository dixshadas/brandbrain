from __future__ import annotations

from typing import Protocol

from brandbrain.platform.auth import Principal

from .schemas import AddEvidenceUnits, Document, EvidenceUnit, RegisterDocument


class EvidenceStore(Protocol):
    async def register_document(self, req: RegisterDocument, principal: Principal) -> Document: ...
    async def get_document(self, document_id: str, principal: Principal) -> Document: ...
    async def add_evidence_units(self, req: AddEvidenceUnits, principal: Principal) -> int: ...
    async def get_evidence_unit(self, unit_id: str, principal: Principal) -> EvidenceUnit:
        """Resolve a citation to its exact span. Powers click-to-source verification."""
        ...
    async def list_documents(self, brand_id: str, principal: Principal) -> list[Document]: ...
