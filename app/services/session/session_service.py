import logging
from uuid import UUID

from app.schemas.session import (
    SessionCreate,
    SessionResponse,
    SessionUpdate,
)

logger = logging.getLogger(__name__)

class SessionService:
    """
    Service responsible for Session business logic.
    """

    def __init__(self, session_repository, transcript_repository):
        """
        Initialize the SessionService with the given repository.
        """
        self.session_repository = session_repository
        self.transcript_repository = transcript_repository

    def _to_response(self, model) -> SessionResponse:
        """
        Convert SQLAlchemy model to Pydantic response.
        """
        return SessionResponse(
            id=model.id,
            user_id=model.user_id,
            transcript_id=model.transcript_id,
            title=model.title,
            summary=model.summary,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def create(
        self,
        *,
        user_id: UUID,
        transcript_id: UUID,
        title: str,
        summary: str | None = None
    ) -> SessionResponse:
        """
        Create a new session.
        """
        transcript = self.transcript_repository.get_by_id(transcript_id, user_id)

        if transcript is None:
            logger.exception(f"Transcript with ID {transcript_id} not found for user {user_id}.")
            raise ValueError(f"Transcript with ID {transcript_id} not found for user {user_id}.")
        
        session_model = self.session_repository.create(
            user_id=user_id,
            transcript_id=transcript_id,
            title=title,
            summary=summary
        )
        return self._to_response(session_model)

    def get_by_id(
        self,
        *,
        session_id: UUID,
        user_id: UUID,
        transcript_id: UUID
    ) -> SessionResponse | None:
        """
        Retrieve a session by its ID.
        """
        transcript = self.transcript_repository.get_by_id(transcript_id, user_id)

        if transcript is None:
            logger.exception(f"Transcript with ID {transcript_id} not found for user {user_id}.")
            raise ValueError(f"Transcript with ID {transcript_id} not found for user {user_id}.")
        
        session_model = self.session_repository.get_by_id(
            session_id=session_id,
            user_id=user_id,
            transcript_id=transcript_id
        )

        if session_model is None:
            logger.warning(
                "Session %s not found for user %s and transcript %s.",
                session_id,
                user_id,
                transcript_id
            )
            return None
        return self._to_response(session_model)

    def get_by_user_id(
        self,
        *,
        user_id: UUID
    ) -> list[SessionResponse]:
        """
        Retrieve all sessions for a specific user.
        """
        session_models = self.session_repository.get_by_user_id(user_id=user_id)
        return [self._to_response(session) for session in session_models]

    def get_by_transcript_id(
        self,
        *,
        user_id: UUID,
        transcript_id: UUID
    ) -> list[SessionResponse]:
        """
        Retrieve all sessions for a specific transcript.
        """
        transcript = self.transcript_repository.get_by_id(transcript_id, user_id)

        if transcript is None:
            logger.exception(f"Transcript with ID {transcript_id} not found for user {user_id}.")
            raise ValueError(f"Transcript with ID {transcript_id} not found for user {user_id}.")
        
        session_models = self.session_repository.get_by_transcript_id(
            transcript_id=transcript_id,
            user_id=user_id
        )
        return [self._to_response(session) for session in session_models]
    

    def update(
        self,
        *,
        session_id: UUID,
        user_id: UUID,
        transcript_id: UUID,
        title: str | None = None,
        summary: str | None = None
    ) -> SessionResponse | None:
        """
        Update an existing session.
        """
        transcript = self.transcript_repository.get_by_id(transcript_id, user_id)

        if transcript is None:
            logger.exception(f"Transcript with ID {transcript_id} not found for user {user_id}.")
            raise ValueError(f"Transcript with ID {transcript_id} not found for user {user_id}.")

        session_model = self.session_repository.update(
            session_id=session_id,
            user_id=user_id,
            transcript_id=transcript_id,
            title=title,
            summary=summary
        )

        if session_model is None:
            logger.warning(
                "Session %s not found for user %s and transcript %s.",
                session_id,
                user_id,
                transcript_id
            )
            return None
        return self._to_response(session_model)

    def delete(
        self,
        *,
        session_id: UUID,
        user_id: UUID,
        transcript_id: UUID
    ) -> bool:
        """
        Delete a session.
        """
        transcript = self.transcript_repository.get_by_id(transcript_id, user_id)

        if transcript is None:
            logger.exception(f"Transcript with ID {transcript_id} not found for user {user_id}.")
            raise ValueError(f"Transcript with ID {transcript_id} not found for user {user_id}.")

        success = self.session_repository.delete(
            session_id=session_id,
            user_id=user_id,
            transcript_id=transcript_id
        )

        if not success:
            logger.warning(
                "Session %s not found for user %s and transcript %s.",
                session_id,
                user_id,
                transcript_id
            )

        return success

    def get_transcript_id_by_session_id(
        self,
        session_id: UUID,
        user_id: UUID
    ) -> UUID | None:
        """
        Retrieve the transcript ID associated with a specific session.
        """
        transcript_id = self.session_repository.get_transcript_id_by_session_id(
            session_id=session_id,
            user_id=user_id
        )

        if transcript_id is None:
            logger.warning(
                "Transcript ID not found for session %s and user %s.",
                session_id,
                user_id
            )
            return None

        return transcript_id

    
    