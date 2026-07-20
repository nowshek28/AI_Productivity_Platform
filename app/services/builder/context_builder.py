import logging

from app.services.retrieval.schemas import RetrievedChunk
from uuid import UUID
from app.services.vector_store.vectorstore_service import VectorStoreService

logger = logging.getLogger(__name__)

class ContextBuilder:
    def __init__(self):
        self.vector_store_service = VectorStoreService()

    def build(
            self,
            retrieved_chunks: list[RetrievedChunk],
            transcript_id: UUID | None = None,
            user_id: UUID | None = None,
    ) -> str:
        """
        Builds a context string from the retrieved chunks.
        """
        try:

            if not retrieved_chunks:
                logger.warning("No retrieved chunks provided to build context.")
                return ""
            
            logger.info(f"Building context from {len(retrieved_chunks)} retrieved chunks.")
            chunks = self._sort_chunks(retrieved_chunks)
            
            chunks = self._expand_neighbors(chunks, transcript_id=transcript_id, user_id=user_id)
            #logger.info(f"Expanded context to {len(chunks)} chunks after including neighbors.")
            chunks = self._deduplicate(chunks)

            chunks = self._merge_consecutive(chunks)

            logger.info(f"Built context Success with {len(chunks)} chunks.")

            return self._format_context(chunks)
        
        except Exception as e:
            logger.exception(f"Error building context: {e}")
            raise RuntimeError(f"Error building context: {e}")

    
    def _sort_chunks(self, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
        """
        Sorts the retrieved chunks based on their relevance score in descending order.
        """
        return sorted(
            chunks, 
            key=lambda chunk: (
                chunk.transcript_id,
                chunk.chunk_index,
            ),
            )
    
    def _format_context(self, chunks: list[RetrievedChunk]) -> str:
        """
        Formats the retrieved chunks into a single context string.
        """
        context_parts = []

        for i, chunk in enumerate(chunks, start=1):

            context_parts.append(
                f"""
===== Context Chunk {i} =====

Filename:
{chunk.filename}

Chunk Index:
{chunk.chunk_index}

Content:
{chunk.document}
""".strip()
            )

        return "\n\n".join(context_parts)
    
    def _expand_neighbors(
        self,
        chunks: list[RetrievedChunk],
        transcript_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> list[RetrievedChunk]:
        # This method is a placeholder for expanding the context by including neighboring chunks by 1.
        expanded_neighbours_chucks = []

        for chunk in chunks:

            result = self.vector_store_service.get_neighboring_chunks(
                transcript_id=str(transcript_id),
                user_id=str(user_id),
                chunk_index=chunk.chunk_index,
                neighbor_range=1,
            )

            for doc, metadata in zip(result["documents"], result["metadatas"]):
                expanded_neighbours_chucks.append(
                    RetrievedChunk(
                        document=doc,
                        distance=0.0,  # Placeholder for distance
                        transcript_id=UUID(metadata["transcript_id"]),
                        chunk_index=metadata["chunk_index"],
                        filename=metadata["filename"],
                    )
                )            

        return expanded_neighbours_chucks


    def _deduplicate(
        self,
        chunks: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        
        # This method is to check whether 2 chuck of same index,
        # is present in the list and remove duplicates.
        seen = set()
        unique_chunks = []
        for chunk in chunks:
            identifier = chunk.chunk_index
            if identifier not in seen:
                seen.add(identifier)
                unique_chunks.append(chunk)

        return unique_chunks


    def _merge_consecutive(
        self,
        chunks: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        return chunks