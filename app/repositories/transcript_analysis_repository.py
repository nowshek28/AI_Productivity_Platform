from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.database.models import TranscriptAnalysisModel

class TranscriptAnalysisRepository:
    def __init__(self, db: Session):
        self.db = db

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
            status: str = "PENDING"
    ) -> TranscriptAnalysisModel:
        """
        Create a new transcript analysis record.
        """

        analysis = TranscriptAnalysisModel(
            transcript_id=str(transcript_id),
            summary=summary,
            sentiment=sentiment,
            sentiment_confidence=sentiment_confidence,
            keywords=keywords,
            entities=entities,
            action_items=action_items,
            analysis_metadata=analysis_metadata,
            status=status,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)

        return analysis

    def get_by_transcript_id(
            self,
            transcript_id: UUID
    ) -> TranscriptAnalysisModel | None:
        """
        Retrieve transcript analysis by transcript ID.
        """

        return (
            self.db.query(TranscriptAnalysisModel)
            .filter(TranscriptAnalysisModel.transcript_id == str(transcript_id))
            .first()
        )

    def update(
            self,
            transcript_id: UUID,
            *,
            summary: str | None = None,
            sentiment: dict | None = None,
            sentiment_confidence: float | None = None,
            keywords: list | None = None,
            entities: dict | None = None,
            action_items: list | None = None,
            analysis_metadata: dict | None = None
    ) -> TranscriptAnalysisModel | None:
        """
        Update an existing transcript analysis record.
        """

        analysis = (
            self.db.query(TranscriptAnalysisModel)
            .filter(TranscriptAnalysisModel.transcript_id == str(transcript_id))
            .first()
        )

        if analysis:
            if summary is not None:
                analysis.summary = summary
            if sentiment is not None:
                analysis.sentiment = sentiment
            if sentiment_confidence is not None:
                analysis.sentiment_confidence = sentiment_confidence
            if keywords is not None:
                analysis.keywords = keywords
            if entities is not None:
                analysis.entities = entities
            if action_items is not None:
                analysis.action_items = action_items
            if analysis_metadata is not None:
                analysis.analysis_metadata = analysis_metadata

            analysis.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(analysis)

        return analysis
    
    def update_status(
            self,
            transcript_id: UUID,
            status: str
    ) -> TranscriptAnalysisModel | None:
        """
        Update the status of a transcript analysis record.
        """

        analysis = (
            self.db.query(TranscriptAnalysisModel)
            .filter(TranscriptAnalysisModel.transcript_id == str(transcript_id))
            .first()
        )

        if analysis:
            analysis.status = status
            analysis.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(analysis)

        return analysis

    def delete_by_transcript_id(
            self,
            transcript_id: UUID
    ) -> bool:
        """
        Delete a transcript analysis record by transcript ID.
        """

        analysis = (
            self.db.query(TranscriptAnalysisModel)
            .filter(TranscriptAnalysisModel.transcript_id == str(transcript_id))
            .first()
        )

        if analysis:
            self.db.delete(analysis)
            self.db.commit()
            return True

        return False