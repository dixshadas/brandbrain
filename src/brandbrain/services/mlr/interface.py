from __future__ import annotations

from typing import Protocol

from brandbrain.platform.auth import Principal

from .schemas import CheckRequest, CheckResponse, LockedClaim, RegisterLockedClaim


class MlrEngine(Protocol):
    async def register_locked_claim(self, req: RegisterLockedClaim, principal: Principal) -> LockedClaim: ...
    async def list_locked_claims(self, brand_id: str, principal: Principal) -> list[LockedClaim]: ...
    async def check(self, req: CheckRequest, principal: Principal) -> CheckResponse:
        """Locked-claim guard (verbatim preserved) + citation-preservation (none dropped).
        Called by Brand Brain before any publish and by the Synthesizer before completing a run.
        """
        ...
