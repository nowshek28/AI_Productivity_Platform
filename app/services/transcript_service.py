import logging
from uuid import UUID

from app.schemas.transcript import (
    TranscriptCreate,
    TranscriptResponse,
)

logger = logging.getLogger(__name__)


class TranscriptService:
    """
    Service responsible for Transcript business logic.
    """

    def __init__(self, transcript_repository, todo_repository):
        """
        Initialize the TranscriptService with the given repositories.
        """
        self.transcript_repository = transcript_repository
        self.todo_repository = todo_repository

    def _to_response(self, model) -> TranscriptResponse:
        """
        Convert SQLAlchemy model to Pydantic response.
        """
        return TranscriptResponse(
            id=model.id,
            todo_id=model.todo_id,
            s3_key=model.s3_key,
            original_filename=model.original_filename,
            file_type=model.file_type,
            file_size=model.file_size,
            uploaded_at=model.uploaded_at,
        )

    def create(
        self,
        todo_id: UUID,
        transcript: TranscriptCreate,
    ) -> TranscriptResponse:
        """
        Create a transcript for a Todo.
        """
        todo = self.todo_repository.get_by_id(todo_id)

        if todo is None:
            logger.warning(
                "Todo %s not found while creating transcript.",
                todo_id,
            )
            return None


        if self.transcript_repository.exists_for_todo(todo_id):
            logger.warning(
                "Transcript already exists for todo %s.",
                todo_id,
            )
            return None

        # --------------------------------------------------
        # Step 3: Upload transcript to S3
        # (Version 2.1)
        # --------------------------------------------------

        # s3_key = self.storage_service.upload_file(...)
        #
        # The upload should:
        #   - Generate a unique S3 object key
        #   - Upload the file
        #   - Return the S3 key
        #
        # For now we use the provided key.

        s3_key = transcript.s3_key

        # --------------------------------------------------
        # Step 4: Save metadata in database
        # --------------------------------------------------

        new_transcript = self.transcript_repository.create(
            todo_id=todo_id,
            s3_key=s3_key,
            original_filename=transcript.original_filename,
            file_type=transcript.file_type,
            file_size=transcript.file_size,
        )

        logger.info(
            "Transcript %s created successfully.",
            new_transcript.id,
        )

        return self._to_response(new_transcript)

    def get_by_id(
        self,
        transcript_id: UUID,
    ) -> TranscriptResponse | None:
        """
        Retrieve transcript by transcript ID.
        """

        transcript = self.transcript_repository.get_by_id(
            transcript_id
        )

        if transcript is None:
            logger.warning(
                "Transcript %s not found.",
                transcript_id,
            )
            return None

        return self._to_response(transcript)

    def get_by_todo_id(
        self,
        todo_id: UUID,
    ) -> TranscriptResponse | None:
        """
        Retrieve transcript associated with a Todo.
        """

        transcript = self.transcript_repository.get_by_todo_id(
            todo_id
        )

        if transcript is None:
            logger.warning(
                "Transcript for todo %s not found.",
                todo_id,
            )
            return None

        return self._to_response(transcript)

    def delete(
        self,
        transcript_id: UUID,
    ) -> bool:
        """
        Delete transcript.
        """

        transcript = self.transcript_repository.get_by_id(
            transcript_id
        )

        if transcript is None:
            logger.warning(
                "Transcript %s not found.",
                transcript_id,
            )
            return False

        # --------------------------------------------------
        # Version 2.1
        # Remove transcript from S3 first.
        # --------------------------------------------------

        # self.storage_service.delete_file(transcript.s3_key)

        self.transcript_repository.delete(transcript)

        logger.info(
            "Transcript %s deleted.",
            transcript_id,
        )

        return True