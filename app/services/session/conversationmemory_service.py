import logging
from uuid import UUID

from app.core.config import settings
from app.schemas.chatmessage import ConversationContext, ChatMessageResponse
from app.services.builder.summary_prompt_builder import SummaryPromptBuilder

logger = logging.getLogger(__name__)

class ConversationMemoryService:

    def __init__(self, chat_message_service, session_service, llm_service):
        self.chatmessage_service = chat_message_service
        self.session_service = session_service
        self.llm_service = llm_service

        self.summary_prompt_builder = SummaryPromptBuilder()

    def update_summary_for_session(
            self,
            session_id: UUID,
            user_id: UUID,
            messages: list
    ):
        try:
            # get the summary from the LLM
            summary_response = self.llm_service.generate_response(
                messages=messages
            )

            # update the summary in the session
            self.session_service.update_summary_by_session_id(
                session_id=session_id,
                user_id=user_id,
                summary=summary_response.answer
            )

            logger.info(
                f"Updated summary for session {session_id} with new summary......."
            )
        except Exception as e:
            logger.exception(f"Error updating summary for session {session_id}: {e}")
            raise RuntimeError(f"Error updating summary for session {session_id}: {e}")
        
    def build_summary_messages(
            self,
            session_id: UUID,
            user_id: UUID
    ) -> list:
        # Implement the logic to update the summary for the given session
        
        try:
            # get context for the summary update
            context = self.get_conversational_context(
                session_id=session_id,
                user_id=user_id
            )

            #normalize the context of last n messages to strings
            last_n_messages_str = self._format_messages(
                messages=[message.dict() for message in context.recent_messages]
            )

            # format the context into a prompt for the LLM
            messages = self.summary_prompt_builder.build_chat_summary(
                previous_summary=context.summary,
                recent_messages=last_n_messages_str
            )

            return messages

        except Exception as e:
            logger.exception(f"Error getting summary context for session {session_id}: {e}")
            raise RuntimeError(f"Error getting summary context for session {session_id}: {e}")

    def should_summarize(
            self,
            session_id: UUID,
    ) -> bool:
        """
        Determine if the conversation memory for a given session should be summarized.
        """

        # Count last messages for the session
        last_messages_count = self.chatmessage_service.count_total_messages(
            session_id=session_id
        )
        
        # if length of last messages is a multiple of CHAT_SUMMARIZATION_THRESHOLD,
        # Send true for a complete set of messages, return True
        if last_messages_count > 0 and last_messages_count % settings.CHAT_SUMMARIZATION_THRESHOLD == 0:
            logger.info(
                f"Conversation memory for session {session_id} has {last_messages_count} messages. Summarization needed."
            )
            return True

        logger.info(
            f"Conversation memory for session {session_id} has {last_messages_count} messages. No summarization needed."
        )
        return False

    def get_conversational_context(
        self,
        *,
        session_id: UUID,
        user_id: UUID,
    ) -> ConversationContext:
        # Implement the logic to retrieve the conversational context for the given session
        # Get summary from sessions
        summary = self.session_service.get_summary_by_session_id(
            session_id=session_id,
            user_id=user_id
        )

        # get last N messages from chatmessage repository
        last_n_messages = self.chatmessage_service.get_last_n_messages(
            session_id=session_id,
            n=settings.CHAT_RECENT_MESSAGE_LIMIT
        )
        ChatMessageResponseList = []

        for message in last_n_messages:
            ChatMessageResponseList.append(
                ChatMessageResponse(
                    id=message.id,
                    session_id=message.session_id,
                    role=message.role,
                    content=message.content,
                    created_at=message.created_at
                )
            )

        #return the summary and list of last N messages as a ConversationContext object
        return ConversationContext(
            summary=summary,
            recent_messages=ChatMessageResponseList
        )

    def _format_messages(
            self,
            messages: list[dict],
    ) -> str:
        # Implement the logic to format messages as needed
        formatted_messages = ""
        for message in messages:
            role = message.get("role")
            content = message.get("content")
            formatted_messages += f"{role.capitalize()}:\n{content}\n\n"
        return formatted_messages
