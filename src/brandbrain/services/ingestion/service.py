"""Implementation notes (stubbed for the scaffold):

Pipeline is event-driven and idempotent per document sha256:
  received -> (parse: PDF/PPTX/DOCX/XLSX/audio) -> evidence units -> metadata proposal
  -> HUMAN GATE -> approved -> embeddings written -> indexed.
Parsers are pluggable; audio uses ASR with word-level timecodes so a quote can cite '00:14:32'.
"""
from __future__ import annotations

from brandbrain.platform.auth import Principal
from brandbrain.platform.eventbus import EventBus
from brandbrain.platform.objectstore import ObjectStore

from .schemas import ConfirmMetadataRequest, IngestJob, StartIngestRequest


class IngestionServiceImpl:
    def __init__(self, bus: EventBus | None = None, store: ObjectStore | None = None) -> None:
        self._bus = bus
        self._store = store

    async def start(self, req: StartIngestRequest, principal: Principal) -> IngestJob:  # pragma: no cover
        raise NotImplementedError("See TDD §Research Ingestion for the pipeline contract.")

    async def get_job(self, job_id: str, principal: Principal) -> IngestJob:  # pragma: no cover
        raise NotImplementedError

    async def confirm_metadata(self, job_id, req: ConfirmMetadataRequest, principal: Principal) -> IngestJob:  # pragma: no cover
        principal.require_role()  # analyst/reviewer; enforced in real impl
        principal.assert_brand(req.brand_id)
        raise NotImplementedError
