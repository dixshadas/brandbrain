"""Vector similarity search behind an interface.

MVP adapter is pgvector (one datastore to run = developer simplicity). The interface is written
so a Qdrant/Weaviate adapter is a drop-in at scale. Retrieval combines this with a lexical (BM25)
signal — see services/retrieval.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class VectorHit:
    evidence_unit_id: str
    score: float
    metadata: dict = field(default_factory=dict)


class VectorStore(Protocol):
    async def upsert(self, brand_id: str, evidence_unit_id: str, vector: list[float], metadata: dict) -> None: ...
    async def query(
        self, brand_id: str, vector: list[float], top_k: int = 20, filters: dict | None = None
    ) -> list[VectorHit]: ...
    async def delete(self, brand_id: str, evidence_unit_id: str) -> None: ...


class InMemoryVectorStore:
    """Cosine similarity over an in-memory dict. Tests + tiny demos only."""

    def __init__(self) -> None:
        self._rows: list[tuple[str, str, list[float], dict]] = []

    async def upsert(self, brand_id, evidence_unit_id, vector, metadata) -> None:
        self._rows = [r for r in self._rows if not (r[0] == brand_id and r[1] == evidence_unit_id)]
        self._rows.append((brand_id, evidence_unit_id, vector, metadata))

    async def query(self, brand_id, vector, top_k=20, filters=None) -> list[VectorHit]:
        def cos(a: list[float], b: list[float]) -> float:
            num = sum(x * y for x, y in zip(a, b, strict=False))
            da = sum(x * x for x in a) ** 0.5 or 1.0
            db = sum(y * y for y in b) ** 0.5 or 1.0
            return num / (da * db)

        scored = [
            VectorHit(uid, cos(vector, vec), meta)
            for (bid, uid, vec, meta) in self._rows
            if bid == brand_id
        ]
        return sorted(scored, key=lambda h: h.score, reverse=True)[:top_k]

    async def delete(self, brand_id, evidence_unit_id) -> None:
        self._rows = [r for r in self._rows if not (r[0] == brand_id and r[1] == evidence_unit_id)]
