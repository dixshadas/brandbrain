from __future__ import annotations

from typing import Protocol

from brandbrain.platform.auth import Principal

from .schemas import SearchRequest, SearchResponse


class RetrievalService(Protocol):
    async def search(self, req: SearchRequest, principal: Principal) -> SearchResponse:
        """Hybrid search, brand-scoped. Every hit carries a Citation (never a bare snippet)."""
        ...
