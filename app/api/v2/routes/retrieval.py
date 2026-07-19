import logging
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from app.schemas.user import CurrentUserResponse
from app.services.retrieval.schemas import SearchRequest, ChatResponse
from app.schemas.transcript import ProcessingStatus
from app.core.config import settings

from app.auth.dependencies import get_current_db_user
from app.core.dependencies import get_transcript_service
from app.core.dependencies import get_retrieval_service

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
        "/transcripts/{transcript_id}/search",
        status_code=200,
        response_model=ChatResponse,
)
async def search_transcript(
    transcript_id: UUID,
    query: SearchRequest,
    retrieval_service=Depends(get_retrieval_service),
    transcript_service=Depends(get_transcript_service),
    current_user: CurrentUserResponse = Depends(get_current_db_user),
):
    """
    Search for relevant information in a specific transcript.
    """
    #ensure transcript exists and belongs to the current user
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
    
    logger.info(f"Searching transcript {transcript_id} for query: {query.query} with top_k={query.top_k}")

    # peform the search using the retrieval service
    chat_response = await retrieval_service.ask(
        query=query.query,
        transcript_id=transcript.id,
        user_id=current_user.id,
        retrieve_top_k = settings.RETRIEVE_TOP_K,
        rerank_top_k=query.top_k
    )

    return ChatResponse(
        answer=chat_response.answer,
        chunks=chat_response.chunks
    )

