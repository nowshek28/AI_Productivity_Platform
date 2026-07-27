import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Response

from app.schemas.user import CurrentUserResponse
from app.schemas.session import SessionCreate, SessionResponse, SessionUpdate
from app.services.retrieval.schemas import SearchRequest, ChatResponse
from app.schemas.transcript import ProcessingStatus
from app.core.config import settings

from app.auth.dependencies import get_current_db_user
from app.core.dependencies import get_transcript_service
from app.core.dependencies import get_retrieval_service
from app.core.dependencies import get_session_service

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    "/transcripts/{transcript_id}/sessions",
    status_code=201,
    response_model=SessionResponse,
)
def create_session(
    transcript_id: UUID,
    session_data: SessionCreate,
    session_service=Depends(get_session_service),
    transcript_service=Depends(get_transcript_service),
    current_user: CurrentUserResponse = Depends(get_current_db_user),
):
    """
    Create a new session for a specific transcript.
    """
    # Ensure transcript exists and belongs to the current user
    transcript = transcript_service.get_by_id(transcript_id, user_id=current_user.id)
    if not transcript:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transcript not found."
        )
    
    if transcript.processing_status != ProcessingStatus.READY:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transcript is still being processed. Please try again later."
        )
    
    logger.info(f"Creating session for transcript {transcript_id} with title: {session_data.title}")

    # Create the session using the session service
    session_response = session_service.create(
        user_id=current_user.id,
        transcript_id=transcript_id,
        title=session_data.title,
        summary=session_data.summary
    )

    return session_response

@router.get(
    "/transcripts/{transcript_id}/sessions",
    status_code=200,
    response_model=list[SessionResponse],
)
def list_sessions(
    transcript_id: UUID,
    session_service=Depends(get_session_service),
    transcript_service=Depends(get_transcript_service),
    current_user: CurrentUserResponse = Depends(get_current_db_user),
):
    """
    List all sessions for a specific transcript.
    """
    # Ensure transcript exists and belongs to the current user
    transcript = transcript_service.get_by_id(transcript_id, user_id=current_user.id)
    if not transcript:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transcript not found."
        )

    return session_service.get_by_transcript_id(transcript_id=transcript_id, user_id=current_user.id)

@router.get(
    "/sessions/{session_id}",
    status_code=200,
    response_model=SessionResponse,
)
def get_session(
    session_id: UUID,
    session_service=Depends(get_session_service),
    current_user: CurrentUserResponse = Depends(get_current_db_user),
):
    """
    Retrieve a specific session by its ID.
    """
    # Ensure transcript exists and belongs to the current user
    transcript_id = session_service.get_transcript_id_by_session_id(session_id, current_user.id)
    if not transcript_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transcript not found."
        )
    

    session_response = session_service.get_by_id(
        session_id=session_id,
        user_id=current_user.id,
        transcript_id=transcript_id
    )
    if not session_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found."
        )
    return session_response

@router.delete(
    "/sessions/{session_id}",
    status_code=204,
)
def delete_session(
    session_id: UUID,
    session_service=Depends(get_session_service),
    current_user: CurrentUserResponse = Depends(get_current_db_user),
):
    """
    Delete a specific session by its ID.
    """
    # Ensure transcript exists and belongs to the current user
    transcript_id = session_service.get_transcript_id_by_session_id(session_id, current_user.id)
    if not transcript_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transcript not found."
        )

    success = session_service.delete(
        session_id=session_id,
        user_id=current_user.id,
        transcript_id=transcript_id
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found."
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post(
    "/sessions/{session_id}/chat",
    status_code=200,
)
def chat_in_session(
    session_id: UUID,
    query: SearchRequest,
    session_service=Depends(get_session_service),
    retrieval_service=Depends(get_retrieval_service),
    current_user: CurrentUserResponse = Depends(get_current_db_user),
):
    """
    Chat within a specific session.
    """
    # Logic will be created here to handle chat within a session, similar to the search_transcript function.


@router.get(
    "/sessions/{session_id}/messages",
    status_code=200,
)
def list_session_messages(
    session_id: UUID,
    session_service=Depends(get_session_service),
    current_user: CurrentUserResponse = Depends(get_current_db_user),
):
    """
    List all messages in a specific session.
    """
    # Logic will be created here to list messages within a session, similar to the list_sessions function.