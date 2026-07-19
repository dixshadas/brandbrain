from __future__ import annotations

from pydantic import BaseModel, Field

from brandbrain.domain.common import Citation, StudyType


class RetrievalFilters(BaseModel):
    study_types: list[StudyType] = Field(default_factory=list)
    suppliers: list[str] = Field(default_factory=list)
    document_ids: list[str] = Field(default_factory=list)


class SearchRequest(BaseModel):
    brand_id: str
    query: str
    top_k: int = Field(default=20, ge=1, le=100)
    filters: RetrievalFilters = Field(default_factory=RetrievalFilters)
    alpha: float = Field(default=0.5, ge=0, le=1, description="vector vs lexical blend (1=vector only)")


class SearchHit(BaseModel):
    citation: Citation
    text: str
    score: float
    vector_score: float
    lexical_score: float


class SearchResponse(BaseModel):
    query: str
    hits: list[SearchHit]
