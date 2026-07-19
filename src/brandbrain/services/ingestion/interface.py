from __future__ import annotations

from typing import Protocol

from brandbrain.platform.auth import Principal

from .schemas import ConfirmMetadataRequest, IngestJob, StartIngestRequest


class IngestionService(Protocol):
    async def start(self, req: StartIngestRequest, principal: Principal) -> IngestJob:
        """Register a document, store the original (write-once), kick off parsing + metadata detect."""
        ...

    async def get_job(self, job_id: str, principal: Principal) -> IngestJob: ...

    async def confirm_metadata(
        self, job_id: str, req: ConfirmMetadataRequest, principal: Principal
    ) -> IngestJob:
        """The governance gate. Emits document.approved -> document.ingested -> document.indexed."""
        ...
