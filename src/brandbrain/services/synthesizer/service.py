"""Orchestration only — the Synthesizer owns no truth of its own.

execute():
  1) Retrieval.search() for each analytical sub-question (brand-scoped).
  2) LLMGateway.complete_structured(response_model=SynthesisOutput) — the model returns typed
     Findings with Citations; it is *not* allowed to emit a claim without evidence (schema-enforced).
  3) TrustEngine.score() assigns Confidence + classifies each Finding's ClaimLayer.
  4) MlrEngine.check() runs locked-claim + citation-preservation guards.
  5) Persist run; publish synthesis.completed. Never publishes to the Brain directly — that is a
     separate, human-gated proposal.
Every LLM call id is recorded so the run is reproducible and auditable.
"""
from __future__ import annotations

from brandbrain.platform.auth import Principal
from brandbrain.platform.eventbus import EventBus
from brandbrain.platform.llm import LLMGateway

from .schemas import RunRequest, SynthesisRun


class SynthesizerServiceImpl:
    def __init__(self, bus: EventBus | None = None, llm: LLMGateway | None = None) -> None:
        self._bus = bus
        self._llm = llm

    async def request_run(self, req: RunRequest, principal: Principal) -> SynthesisRun:  # pragma: no cover
        principal.assert_brand(req.brand_id)
        req.validate_scope()  # confirmation-before-execution is enforced here, not in the UI
        raise NotImplementedError("Enqueue run + emit synthesis.requested; see TDD §Synthesizer.")

    async def get_run(self, run_id, principal: Principal) -> SynthesisRun:  # pragma: no cover
        raise NotImplementedError

    async def execute(self, run_id: str) -> SynthesisRun:  # pragma: no cover
        raise NotImplementedError
