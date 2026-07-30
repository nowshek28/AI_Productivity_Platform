import logging

from app.celery.celery_app import celery_app

from app.services.session.conversationmemory_service import ConversationMemoryService
from app.services.session.session_service import SessionService
from app.services.session.chatmessage_service import ChatMessageService
from app.services.llm.llm_service import LLMService

from app.repositories.chatmessage_repository import ChatMessageRepository
from app.repositories.session_repository import SessionRepository
from app.repositories.transcript_repository import TranscriptRepository

from app.database.database import get_db

logger = logging.getLogger(__name__)

@celery_app.task(name="summarize_conversation_memory")
def summarize_conversation_memory(
    session_id: str,
    user_id: str,
):
    """
    Celery task to summarize conversation memory.

    Args:
        session_id (str): The ID of the session to summarize.
        user_id (str): The ID of the user who owns the session.
        messages (list): The list of messages to summarize.
    """
    

    # Initialize services
    db = next(get_db())

    chatmessage_service = ChatMessageService(
        chatmessage_repository=ChatMessageRepository(db=db)
    )
    session_service = SessionService(
        session_repository=SessionRepository(db=db),
        transcript_repository=TranscriptRepository(db=db)
    )
    llm_service = LLMService()
    conversation_memory_service = ConversationMemoryService(
                chat_message_service=chatmessage_service,
                session_service=session_service,
                llm_service=llm_service
            )

    try:
        
        # Get the messages for the session
        messages = conversation_memory_service.build_summary_messages(
            session_id=session_id,
            user_id=user_id
        )

        logger.info(f"Retrieved {len(messages)} messages for session {session_id} to summarize.")

        # Update the summary for the session
        conversation_memory_service.update_summary_for_session(
            session_id=session_id,
            user_id=user_id,
            messages=messages
        )

        # Log the successful completion of the summarization task
        logger.info(f"Successfully summarized conversation memory for session {session_id}.")

    except Exception as e:
        logger.exception(f"Error summarizing conversation memory for session {session_id}: {e}")
        raise RuntimeError(f"Error summarizing conversation memory for session {session_id}: {e}")

    finally:
        # Clean up resources if needed
        pass
