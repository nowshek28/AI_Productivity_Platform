import logging
from uuid import UUID

from app.schemas.chatmessage import (
    ChatMessageCreate,
    ChatMessageResponse,
)

class ChatMessageService:
    """
    Service responsible for ChatMessage business logic.
    """

    def __init__(self, chatmessage_repository):
        """
        Initialize the ChatMessageService with the given repository.
        """
        self.chatmessage_repository = chatmessage_repository

    def _to_response(self, model) -> ChatMessageResponse:
        """
        Convert SQLAlchemy model to Pydantic response.
        """
        return ChatMessageResponse(
            id=model.id,
            session_id=model.session_id,
            role=model.role,
            content=model.content,
            created_at=model.created_at
        )

    def create(
        self,
        *,
        session_id: UUID,
        role: str,
        content: str
    ) -> ChatMessageResponse:
        """
        Create a new chat message.
        """
        chat_message_model = self.chatmessage_repository.create(
            session_id=session_id,
            role=role,
            content=content
        )
        return self._to_response(chat_message_model)

    def get_by_session_id(
        self,
        *,
        session_id: UUID
    ) -> list[ChatMessageResponse]:
        """
        Retrieve chat messages by session ID.
        """
        chat_message_models = self.chatmessage_repository.get_by_session_id(
            session_id=session_id
        )
        return [self._to_response(model) for model in chat_message_models]

    def get_by_id(
        self,
        *,
        id: UUID,
        session_id: UUID
    ) -> ChatMessageResponse | None:
        """
        Retrieve a chat message by its ID.
        """
        chat_message_model = self.chatmessage_repository.get_by_id(
            id=id,
            session_id=session_id
        )
        if chat_message_model is None:
            return None
        return self._to_response(chat_message_model)

    def get_last_n_messages(
        self,
        *,
        session_id: UUID,
        n: int
    ) -> list[ChatMessageResponse]:
        """
        Retrieve the last N chat messages for a given session ID.
        """
        chat_message_models = self.chatmessage_repository.get_last_n_messages(
            session_id=session_id,
            n=n
        )
        return [self._to_response(model) for model in chat_message_models]

    def delete(
        self,
        *,
        session_id: UUID
    ) -> bool:
        """
        Delete a chat message by its session ID.
        """
        success = self.chatmessage_repository.delete_by_session_id(
            session_id=session_id
        )

        if not success:
            logging.warning(
                "Chat message not found for session %s.",
                session_id
            )

        return success
