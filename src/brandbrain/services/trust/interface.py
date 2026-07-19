from __future__ import annotations

from typing import Protocol

from brandbrain.domain.common import Confidence

from .schemas import ClassifyRequest, ClassifyResponse, ScoreRequest


class TrustEngine(Protocol):
    async def score(self, req: ScoreRequest) -> Confidence:
        """Compute an explainable, capped Confidence from the evidence signals."""
        ...

    async def classify(self, req: ClassifyRequest) -> ClassifyResponse:
        """Assign FACT / INSIGHT / INTERPRETATION / RECOMMENDATION to a statement."""
        ...
