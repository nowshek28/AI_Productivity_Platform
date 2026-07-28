from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from app.services.retrieval.schemas import RetrievedChunk

class MessageRole(str):
    USER = "user"
    AI = "ai"

class ChatMessageBase(BaseModel):
    """Base schema for chat message"""

    session_id: UUID = Field(
        ...,
        description="Session ID associated with the chat message"
    )

    role: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Role of the chat message sender (e.g., user, AI)"
    )

    content: str = Field(
        ...,
        min_length=1,
        description="Content of the chat message"
    )

class ChatMessageCreate(ChatMessageBase):
    """Schema for creating a chat message"""

    pass

class ChatSearchRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        description="Search query for the chat message"
    )
    top_k: int = Field(
        5,
        ge=1,
        le=20,
        description="Number of top results to retrieve"
    )

class ChatMessageResponse(ChatMessageBase):
    """Schema for chat message response"""

    id: UUID
    session_id: UUID
    role: str
    content: str
    created_at: datetime

class ChatResponse(BaseModel):
    id: UUID
    session_id: UUID
    role: str
    answer: str
    chunks: list[RetrievedChunk]

class ChatSessionResponse(BaseModel):
    user_message: ChatMessageResponse
    ai_message: ChatResponse

class ConversationContext(BaseModel):
    summary: str | None
    recent_messages: list[ChatMessageResponse]