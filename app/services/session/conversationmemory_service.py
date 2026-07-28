import logging
from uuid import UUID

from app.core.config import settings
from app.schemas.chatmessage import ConversationContext

class ConversationMemoryService:
    def should_summarize(
            self,
            session_id: UUID,
    ) -> bool:
        """
        Determine if the conversation memory for a given session should be summarized.
        """

        # Count last messages for the session
        last_messages_count = self.chatmessage_repository.count_total_messages(
            session_id=session_id
        )
        
        # if length of last messages is a multiple of CHAT_SUMMARIZATION_THRESHOLD,
        # Send true for a complete set of messages, return True
        if last_messages_count % settings.CHAT_SUMMARIZATION_THRESHOLD == 0:
            logging.info(
                f"Conversation memory for session {session_id} has {last_messages_count} messages. Summarization needed."
            )
            return True

        logging.info(
            f"Conversation memory for session {session_id} has {last_messages_count} messages. No summarization needed."
        )
        return False

    def get_conversational_context(
        self,
        *,
        session_id: UUID,
    ) -> ConversationContext:
        # Implement the logic to retrieve the conversational context for the given session
        # call LLM to summarize with last N messages,
        # return the summary and last N messages as a ConversationContext object
        
        pass