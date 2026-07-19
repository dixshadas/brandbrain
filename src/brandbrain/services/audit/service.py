from __future__ import annotations

import hashlib
import json

from brandbrain.platform.auth import Principal

from .schemas import AppendRecord, AuditRecord, VerifyResponse


def compute_hash(prev_hash: str, payload: dict) -> str:
    body = prev_hash + json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode()).hexdigest()


class AuditEngineImpl:
    """Consumes every domain event and also exposes an explicit append() for in-process actions.
    The chain makes the audit trail tamper-evident (see TDD §Audit Engine).
    """

    async def append(self, rec: AppendRecord) -> AuditRecord:  # pragma: no cover
        raise NotImplementedError("Fetch last hash for brand, compute_hash(), INSERT-only.")

    async def list_for_target(self, target_id, principal: Principal) -> list[AuditRecord]:  # pragma: no cover
        raise NotImplementedError

    async def verify_chain(self, brand_id, principal: Principal) -> VerifyResponse:  # pragma: no cover
        raise NotImplementedError
