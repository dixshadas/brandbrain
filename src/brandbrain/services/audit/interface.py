from __future__ import annotations

from typing import Protocol

from brandbrain.platform.auth import Principal

from .schemas import AppendRecord, AuditRecord, VerifyResponse


class AuditEngine(Protocol):
    async def append(self, rec: AppendRecord) -> AuditRecord:
        """Append one record, chaining its hash to the previous. Never updates or deletes."""
        ...
    async def list_for_target(self, target_id: str, principal: Principal) -> list[AuditRecord]: ...
    async def verify_chain(self, brand_id: str, principal: Principal) -> VerifyResponse:
        """Recompute the hash chain to prove the log has not been tampered with."""
        ...
