from __future__ import annotations

from brandbrain.platform.auth import Principal
from brandbrain.platform.llm import LLMGateway
from brandbrain.platform.vectorstore import VectorStore

from .schemas import SearchRequest, SearchResponse


class RetrievalServiceImpl:
    """Hybrid ranking: reciprocal-rank-fusion of pgvector cosine hits and a BM25 lexical pass,
    blended by `alpha`, then hydrated into Citations from the Evidence Store. See TDD §Retrieval.
    """

    def __init__(self, vectors: VectorStore | None = None, llm: LLMGateway | None = None) -> None:
        self._vectors = vectors
        self._llm = llm

    async def search(self, req: SearchRequest, principal: Principal) -> SearchResponse:  # pragma: no cover
        principal.assert_brand(req.brand_id)
        raise NotImplementedError("RRF(vector, bm25) then hydrate citations; see TDD §Retrieval.")
