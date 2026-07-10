from fastapi import APIRouter, Depends, status
from fastapi.responses import Response
from uuid import UUID

from app.schemas.transcript import TranscriptResponse
from app.schemas.user import CurrentUserResponse
from app.services.todo_service import TodoService
from app.core.dependencies import get_service
from app.auth.dependencies import get_current_db_user
from app.core.dependencies import get_transcript_service


router = APIRouter()

@router.post(
        "/todos/{todo_id}/transcript",
        response_model=TranscriptResponse,
        status_code=200,
        )
def create_transcript_for_todo(
    todo_id: UUID,
    transcript_service=Depends(get_transcript_service),
    service: TodoService = Depends(get_service),
    current_user: CurrentUserResponse = Depends(get_current_db_user),
):
    """
    Create a transcript for a specific Todo.
    """
    # Ensure the todo exists and belongs to the current user
    todo = service.get_by_id(todo_id, user_id=current_user.id)
    if not todo:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    # Create the transcript
    transcript = transcript_service.create(todo_id)
    if not transcript:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    return transcript

@router.get(
        "/todos/{todo_id}/transcript",
        response_model=TranscriptResponse,
        status_code=200,
        )
def get_transcript_for_todo(
    todo_id: UUID,
    transcript_service=Depends(get_transcript_service),
    service: TodoService = Depends(get_service),
    current_user: CurrentUserResponse = Depends(get_current_db_user),
):
    """
    Get the transcript for a specific Todo.
    """
    # Ensure the todo exists and belongs to the current user
    todo = service.get_by_id(todo_id, user_id=current_user.id)
    if not todo:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    # Get the transcript
    transcript = transcript_service.get_by_todo_id(todo_id)
    if not transcript:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return transcript

@router.delete(
        "/transcripts/{transcript_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        )
def delete_transcript_for_todo(
    transcript_id: UUID,
    transcript_service=Depends(get_transcript_service),
    service: TodoService = Depends(get_service),
    current_user: CurrentUserResponse = Depends(get_current_db_user),
):
    """
    Delete the transcript for a specific Todo.
    """

    # Get the transcript
    transcript = transcript_service.get_by_id(transcript_id)
    if not transcript:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    # Delete the transcript
    success = transcript_service.delete(transcript.id)
    if not success:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    

@router.get(
        "/transcripts/{transcript_id}",
        response_model=TranscriptResponse,
        status_code=200,
        )   
def get_transcript_by_id(
    transcript_id: UUID,
    transcript_service=Depends(get_transcript_service),
):
    """
    Get a transcript by its ID.
    """
    transcript = transcript_service.get_by_id(transcript_id)
    if not transcript:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return transcript
                                        