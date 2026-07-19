from pydantic import BaseModel, Field
from uuid import UUID

class RetrievedChunk(BaseModel):

    document: str

    distance: float
    
    rerank_score: float | None = None

    transcript_id: UUID

    chunk_index: int

    filename: str

class SearchRequest(BaseModel):

    query: str

    transcript_id: UUID | None = None

    top_k: int = Field(default=5, ge=1, le=20)

class SearchResponse(BaseModel):

    query: str

    results: list[RetrievedChunk]

class BuiltContext(BaseModel):

    context: str

    chunk_count: int
    
    sources: list[RetrievedChunk]


class LLMResponse(BaseModel):

    answer: str

    model: str

class ChatResponse(BaseModel):

    answer: str

    chunks: list[RetrievedChunk]