import logging
from uuid import UUID

from app.schemas.transcript_analysis import (
    TranscriptAnalysisCreate,
    TranscriptAnalysisResponse,
    TranscriptAnalysisUpdate,
)

logger = logging.getLogger(__name__)

class TranscriptAnalysisService:
    """
    Service responsible for Transcript Analysis business logic.
    """

    def __init__(self, transcript_analysis_repository):
        """
        Initialize the TranscriptAnalysisService with the given repository.
        """
        self.transcript_analysis_repository = transcript_analysis_repository

    def _to_response(self, model) -> TranscriptAnalysisResponse:
        """
        Convert SQLAlchemy model to Pydantic response.
        """
        return TranscriptAnalysisResponse(
            id=model.id,
            transcript_id=model.transcript_id,
            summary=model.summary,
            sentiment=model.sentiment,
            sentiment_confidence=model.sentiment_confidence,
            keywords=model.keywords,
            entities=model.entities,
            action_items=model.action_items,
            analysis_metadata=model.analysis_metadata,
            status=model.status
        )

    def create(
        self,
        *,
        transcript_id: UUID,
        summary: str | None = None,
        sentiment: dict | None = None,
        sentiment_confidence: float | None = None,
        keywords: list | None = None,
        entities: dict | None = None,
        action_items: list | None = None,
        analysis_metadata: dict | None = None,
        status: str | None = None
    ) -> TranscriptAnalysisResponse:
        """
        Create a new transcript analysis.
        """
        transcript_analysis_model = self.transcript_analysis_repository.create(
            transcript_id=transcript_id,
            summary=summary,
            sentiment=sentiment,
            sentiment_confidence=sentiment_confidence,
            keywords=keywords,
            entities=entities,
            action_items=action_items,
            analysis_metadata=analysis_metadata,
            status=status
        )
        return self._to_response(transcript_analysis_model)

    def get_by_id(
        self,
        *,
        transcript_analysis_id: UUID
    ) -> TranscriptAnalysisResponse:
        """
        Get a transcript analysis by its ID.
        """
        transcript_analysis_model = self.transcript_analysis_repository.get_by_id(transcript_analysis_id)

        if transcript_analysis_model is None:
            logger.exception(f"Transcript analysis with ID {transcript_analysis_id} not found.")
            return None

        return self._to_response(transcript_analysis_model)

    def update(
        self,
        *,
        transcript_analysis_id: UUID,
        summary: str | None = None,
        sentiment: dict | None = None,
        sentiment_confidence: float | None = None,
        keywords: list | None = None,
        entities: dict | None = None,
        action_items: list | None = None,
        analysis_metadata: dict | None = None,
        status: str | None = None
    ) -> TranscriptAnalysisResponse:
        """
        Update an existing transcript analysis.
        """
        transcript_analysis_model = self.transcript_analysis_repository.update(
            transcript_analysis_id=transcript_analysis_id,
            summary=summary,
            sentiment=sentiment,
            sentiment_confidence=sentiment_confidence,
            keywords=keywords,
            entities=entities,
            action_items=action_items,
            analysis_metadata=analysis_metadata,
            status=status
        )

        if transcript_analysis_model is None:
            logger.exception(f"Transcript analysis with ID {transcript_analysis_id} not found for update.")
            return None

        return self._to_response(transcript_analysis_model)

    def update_status(
        self,
        *,
        transcript_analysis_id: UUID,
        status: str
    ) -> TranscriptAnalysisResponse:
        """
        Update the status of an existing transcript analysis.
        """
        transcript_analysis_model = self.transcript_analysis_repository.update_status(
            transcript_analysis_id=transcript_analysis_id,
            status=status
        )

        if transcript_analysis_model is None:
            logger.exception(f"Transcript analysis with ID {transcript_analysis_id} not found for status update.")
            return None

        return self._to_response(transcript_analysis_model)

    
    def delete(
        self,
        *,
        transcript_analysis_id: UUID
    ) -> bool:
        """
        Delete a transcript analysis by its ID.
        """
        success = self.transcript_analysis_repository.delete(transcript_analysis_id)
        if not success:
            logger.exception(f"Transcript analysis with ID {transcript_analysis_id} not found for deletion.")
        return success