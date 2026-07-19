import logging

from sentence_transformers import cross_encoder

from app.services.retrieval.schemas import RetrievedChunk
from app.core.config import settings

logger = logging.getLogger(__name__)

class CrossEncoderService:
    def __init__(self):
        self.provider = settings.EMBEDDING_PROVIDER
        self.model_name = settings.CROSS_ENCODER_MODEL
        # Initialize the cross-encoder model here (e.g., load from Hugging Face)

        if self.provider == "huggingface":
            self.model = cross_encoder.CrossEncoder(self.model_name)
        else:
            self.model = None
            logger.warning("Cross-encoder model is not initialized. Unsupported provider: %s", self.provider)

    async def rerank(
            self, 
            query: str, 
            results: list[RetrievedChunk],
            top_k: int = 5
        ) -> list[RetrievedChunk]:
        """
        Rerank the search results based on the query using a cross-encoder model.

        :param query: The search query.
        :param results: A list of search results, each result is a dictionary containing 'chunk' and 'score'.
        :return: A list of reranked search results.
        """
        pairs = [(query, result.document) for result in results]
        # Compute relevance scores using the cross-encoder model

        scores = self.model.predict(pairs)  # Replace with actual model prediction

        scored_results = list(zip(results, scores))
        scored_results.sort(key=lambda x: x[1], reverse=True)
        
        filtered_result = [
            RetrievedChunk(
                document=result.document,
                distance=getattr(result, 'distance', 0.0),
                rerank_score=score,
                transcript_id=result.transcript_id,
                chunk_index=result.chunk_index,
                filename=result.filename,
            )
            for result, score in scored_results[:top_k]
            if score >= settings.RERANK_SCORE_THRESHOLD
        ]

        if not filtered_result:
            logger.warning("No results met the rerank score threshold of %f.", settings.RERANK_SCORE_THRESHOLD)
            return []
        
        logger.info("Reranked %d results based on the query.", len(filtered_result))
        return filtered_result