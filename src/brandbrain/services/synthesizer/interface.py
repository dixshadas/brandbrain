from __future__ import annotations

from typing import Protocol

from brandbrain.platform.auth import Principal

from .schemas import RunRequest, SynthesisRun


class SynthesizerService(Protocol):
    async def request_run(self, req: RunRequest, principal: Principal) -> SynthesisRun:
        """Validate scope, enqueue the run (async), return a QUEUED run. Emits synthesis.requested."""
        ...

    async def get_run(self, run_id: str, principal: Principal) -> SynthesisRun: ...

    async def execute(self, run_id: str) -> SynthesisRun:
        """Worker entrypoint: retrieve -> reason -> classify (Trust) -> check (MLR) -> persist.
        Emits synthesis.completed | synthesis.failed.
        """
        ...
