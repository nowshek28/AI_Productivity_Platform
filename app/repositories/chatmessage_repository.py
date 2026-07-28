from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.database.models import ChatMessageModel

class ChatMessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
            self,
            *,
            session_id: UUID,
            role: str,
            content: str
    ) -> ChatMessageModel:
        """
        Create a new chat message record.
        """

        chat_message = ChatMessageModel(
            session_id=str(session_id),
            role=role,
            content=content
        )

        self.db.add(chat_message)
        self.db.commit()
        self.db.refresh(chat_message)

        return chat_message

    def get_by_session_id(
            self,
            session_id: UUID
    ) -> list[ChatMessageModel]:
        """
        Retrieve chat messages by session ID.
        """

        return (
            self.db.query(ChatMessageModel)
            .filter(ChatMessageModel.session_id == str(session_id))
            .order_by(ChatMessageModel.created_at.asc())
            .all()
        )

    def get_by_id(
            self,
            id: UUID,
            session_id: UUID
    ) -> ChatMessageModel | None:
        """
        Retrieve chat message by ID.
        """

        return (
            self.db.query(ChatMessageModel)
            .filter(ChatMessageModel.id == str(id))
            .filter(ChatMessageModel.session_id == str(session_id))
            .first()
        )

    def get_last_n_messages(
            self,
            session_id: UUID,
            n: int
    ) -> list[ChatMessageModel]:
        """
        Retrieve the last N chat messages for a specific session.
        """

        messages = (
            self.db.query(ChatMessageModel)
            .filter(ChatMessageModel.session_id == str(session_id))
            .order_by(ChatMessageModel.created_at.desc())
            .limit(n)
            .all()
        )

        messages.reverse()

        return messages

    def delete_by_session_id(
            self,
            session_id: UUID
    ) -> bool:
        """
        Delete all chat messages by session ID.
        """
        chat_messages = (
            self.db.query(ChatMessageModel)
            .filter(ChatMessageModel.session_id == str(session_id))
            .all()
        )

        if not chat_messages:
            return False

        for chat_message in chat_messages:
            self.db.delete(chat_message)
        self.db.commit()

        return True

    def count_total_messages(
            self,
            session_id: UUID
    ) -> int:
        """
        Count the total number of chat messages for a specific session.
        """

        return (
            self.db.query(ChatMessageModel)
            .filter(ChatMessageModel.session_id == str(session_id))
            .count()
        )
    