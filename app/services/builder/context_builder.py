import logging

from app.services.retrieval.schemas import RetrievedChunk

logger = logging.getLogger(__name__)

class ContextBuilder:
    def build(
            self,
            retrieved_chunks: list[RetrievedChunk],
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
            
            chunks = self._expand_neighbors(chunks)

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
    ) -> list[RetrievedChunk]:
        return chunks


    def _deduplicate(
        self,
        chunks: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        return chunks


    def _merge_consecutive(
        self,
        chunks: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        return chunks