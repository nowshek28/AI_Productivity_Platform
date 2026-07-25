from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.database.models import SessionModel

class SessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
            self,
            *,
            user_id: UUID,
            transcript_id: UUID,
            title: str,
            summary: str | None = None
    ) -> SessionModel:
        """
        Create a new session record.
        """

        session = SessionModel(
            user_id=str(user_id),
            transcript_id=str(transcript_id),
            title=title,
            summary=summary
        )

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session

    def get_by_id(
            self,
            session_id: UUID,
            user_id: UUID,
            transcript_id: UUID,
    ) -> SessionModel | None:
        """
        Retrieve session by session ID.
        """

        return (
            self.db.query(SessionModel)
            .filter(SessionModel.id == str(session_id))
            .filter(SessionModel.user_id == str(user_id))
            .filter(SessionModel.transcript_id == str(transcript_id))
            .first()
        )

    def get_by_user_id(
            self,
            user_id: UUID
    ) -> list[SessionModel]:
        """
        Retrieve all sessions for a specific user.
        """

        return (
            self.db.query(SessionModel)
            .filter(SessionModel.user_id == str(user_id))
            .all()
        )

    def get_by_transcript_id(
            self,
            transcript_id: UUID,
            user_id: UUID
    ) -> list[SessionModel]:
        """
        Retrieve all sessions for a specific transcript.
        """

        return (
            self.db.query(SessionModel)
            .filter(SessionModel.transcript_id == str(transcript_id))
            .filter(SessionModel.user_id == str(user_id))
            .all()
        )

    def delete(
            self,
            session_id: UUID,
            user_id: UUID,
            transcript_id: UUID,
    ) -> bool:
        """
        Delete a session by session ID and user ID.
        """

        session = (
            self.db.query(SessionModel)
            .filter(SessionModel.id == str(session_id))
            .filter(SessionModel.user_id == str(user_id))
            .filter(SessionModel.transcript_id == str(transcript_id))
            .first()
        )

        if not session:
            return False

        self.db.delete(session)
        self.db.commit()

        return True

    def update(
            self,
            session_id: UUID,
            user_id: UUID,
            transcript_id: UUID,
            title: str | None = None,
            summary: str | None = None
    ) -> SessionModel | None:
        """
        Update a session's title and/or summary.
        """

        session = (
            self.db.query(SessionModel)
            .filter(SessionModel.id == str(session_id))
            .filter(SessionModel.user_id == str(user_id))
            .filter(SessionModel.transcript_id == str(transcript_id))
            .first()
        )

        if not session:
            return None

        if title is not None:
            session.title = title
        if summary is not None:
            session.summary = summary

        self.db.commit()
        self.db.refresh(session)

        return session

    def get_transcript_id_by_session_id(
            self,
            session_id: UUID,
            user_id: UUID
    ) -> UUID | None:
        """
        Retrieve the transcript ID associated with a given session ID.
        """

        session = (
            self.db.query(SessionModel)
            .filter(SessionModel.id == str(session_id))
            .filter(SessionModel.user_id == str(user_id))
            .first()
        )

        if not session:
            return None

        return UUID(session.transcript_id)