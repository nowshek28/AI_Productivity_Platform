from uuid import UUID
from app.celery.tasks.chat_summary_tasks import summarize_conversation_memory

def summarize_conversation_chat(self, session_id: UUID, user_id: UUID) -> None:
        """
        Trigger the summarization of conversation memory for a given session.
        """
        #call the Celery task to summarize the conversation memory
        summarize_conversation_memory.delay(session_id, user_id)