"""The LLM gateway. The ONLY place the app talks to a model provider.

Two hard rules that make trust auditable:
  1) Every call is structured: the caller passes a Pydantic response schema and gets a validated
     object back (via `instructor`), never free text we have to parse hopefully.
  2) Every call is traced: prompt hash, model, tokens, latency, and cost are recorded so any AI
     output in the product can be reproduced and explained (see Audit + Trust engines).
Providers (Anthropic/OpenAI/Bedrock/Azure) sit behind litellm, so switching models is config.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


@dataclass(frozen=True)
class LLMCallRecord:
    """Emitted for every call; consumed by the Audit + Trust engines."""
    call_id: str
    model: str
    prompt_sha256: str
    input_tokens: int
    output_tokens: int
    latency_ms: int
    cost_usd: float


class LLMGateway(Protocol):
    async def complete_structured(
        self,
        *,
        model: str,
        system: str,
        prompt: str,
        response_model: type[T],
        temperature: float = 0.0,
        max_tokens: int = 4096,
    ) -> tuple[T, LLMCallRecord]:
        """Return a validated response object plus a reproducibility record."""
        ...

    async def embed(self, texts: list[str], *, model: str) -> list[list[float]]: ...


class StubLLMGateway:
    """Deterministic stub for tests/scaffold. Returns model defaults; records a fake call."""

    async def complete_structured(self, *, model, system, prompt, response_model, temperature=0.0, max_tokens=4096):
        import hashlib

        rec = LLMCallRecord(
            call_id="llmcall_stub",
            model=model,
            prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),
            input_tokens=len(prompt) // 4,
            output_tokens=0,
            latency_ms=0,
            cost_usd=0.0,
        )
        return response_model.model_construct(), rec

    async def embed(self, texts, *, model):
        return [[0.0] * 8 for _ in texts]
