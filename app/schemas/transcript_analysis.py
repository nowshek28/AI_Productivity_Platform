from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class TranscriptAnalysisBase(BaseModel):
    """Base schema for transcript analysis"""

    transcript_id: UUID = Field(
        ...,
        description="Transcript ID associated with the analysis"
    )

    summary: str | None = Field(
        None,
        description="Summary of the transcript analysis"
    )

    sentiment: dict | None = Field(
        None,
        description="Sentiment analysis result of the transcript"
    )

    sentiment_confidence: float | None = Field(
        None,
        description="Confidence score of the sentiment analysis"
    )

    keywords: list | None = Field(
        None,
        description="List of keywords extracted from the transcript"
    )

    entities: dict | None = Field(
        None,
        description="Entities extracted from the transcript"
    )

    action_items: list | None = Field(
        None,
        description="List of action items extracted from the transcript"
    )

    analysis_metadata: dict | None = Field(
        None,
        description="Metadata related to the transcript analysis"
    )

    status: str = Field(
        "PENDING",
        description="Status of the transcript analysis"
    )

class TranscriptAnalysisCreate(TranscriptAnalysisBase):
    """Schema for creating a new transcript analysis"""
    pass

class TranscriptAnalysisUpdate(BaseModel):
    """Schema for updating an existing transcript analysis"""

    summary: str | None = Field(
        None,
        description="Summary of the transcript analysis"
    )

    sentiment: dict | None = Field(
        None,
        description="Sentiment analysis result of the transcript"
    )

    sentiment_confidence: float | None = Field(
        None,
        description="Confidence score of the sentiment analysis"
    )

    keywords: list | None = Field(
        None,
        description="List of keywords extracted from the transcript"
    )

    entities: dict | None = Field(
        None,
        description="Entities extracted from the transcript"
    )

    action_items: list | None = Field(
        None,
        description="List of action items extracted from the transcript"
    )

    analysis_metadata: dict | None = Field(
        None,
        description="Metadata related to the transcript analysis"
    )

    status: str | None = Field(
        None,
        description="Status of the transcript analysis"
    )

class TranscriptAnalysisResponse(TranscriptAnalysisBase):
    """Schema for transcript analysis response"""

    id: UUID
    transcript_id: UUID
    summary: str | None
    sentiment: dict | None
    sentiment_confidence: float | None
    keywords: list | None
    entities: dict | None
    action_items: list | None
    analysis_metadata: dict | None
    status: str
    created_at: datetime
    updated_at: datetime