from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class SessionBase(BaseModel):
    """Base schema for session"""

    transcript_id: UUID = Field(
        ...,
        description="Transcript ID associated with the session"
    )

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Title of the session"
    )

    summary: str | None = Field(
        None,
        description="Summary of the session"
    )

class SessionCreate(SessionBase):
    """Schema for creating a new session"""
    pass

class SessionUpdate(BaseModel):
    """Schema for updating an existing session"""

    title: str | None = Field(
        None,
        min_length=1,
        max_length=255,
        description="Title of the session"
    )

    summary: str | None = Field(
        None,
        description="Summary of the session"
    )

class SessionResponse(SessionBase):
    """Schema for session response"""

    id: UUID
    transcript_id: UUID
    title: str
    summary: str | None
    created_at: datetime
    updated_at: datetime

