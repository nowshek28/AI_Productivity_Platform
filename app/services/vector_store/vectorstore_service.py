import logging
from uuid import UUID

import chromadb

from app.core.config import settings
logger = logging.getLogger(__name__)

class VectorStoreService:

    def __init__(self):
        client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self.collection = client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME
        )

    def prepare_records(
            self,
            transcript,
            chunks: list[str],
            embeddings: list[list[float]],
    ) -> list[dict]:
        """
        Prepares records for insertion into the vector store.

        Args:
            transcript: The transcript object containing metadata.
            chunks (list[str]): The text chunks to be stored.
            embeddings (list[list[float]]): The corresponding embeddings for the chunks.
        """
        if len(chunks) != len(embeddings):
            logger.error("The number of chunks and embeddings must be the same.")
            raise ValueError("The number of chunks and embeddings must be the same.")

        records = []
        for chunk_index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            record = {
                "id": (
                    f"transcript_{transcript.id}"
                    f"_chunk_{chunk_index}"
                ),
                "document": chunk,
                "embedding": embedding,
                "metadata": {
                    "transcript_id": transcript.id,
                    "todo_id": transcript.todo_id,
                    "user_id": transcript.user_id,
                    "filename": transcript.original_filename,
                    "file_type": transcript.file_type,
                    "chunk_index": chunk_index,
                    "embedding_model": settings.EMBEDDING_MODEL,
                },
            }
            records.append(record)
        
        logger.info("Prepared %d records for vector store insertion.", len(records))
        return records
    
    def store_records(self, records: list[dict]):
        """
        Stores the prepared records into the vector store.

        Args:
            records (list[dict]): The records to be stored.
        """
        try:
            if not records:
                logger.warning("No records to store in the vector store.")
                return
            
            logger.info("Storing %d records in the vector store.", len(records))

            self.collection.add(
                ids=[r["id"] for r in records],
                documents=[r["document"] for r in records],
                embeddings=[r["embedding"] for r in records],
                metadatas=[r["metadata"] for r in records],
            )

            logger.info("Successfully stored %d records in the vector store.", len(records))
        except Exception as e:
            logger.error("Failed to store records in the vector store: %s", str(e))
            raise RuntimeError("Failed to store records in the vector store.") from e
        
    async def search(
            self,
            query_embedding: list[float],
            where: dict | None = None,
            include: list[str] | None = None,
            top_k: int = 10,
    ) -> dict:
        """
        Searches the vector store for records similar to the provided query embedding.

        Args:
            query_embedding (list[float]): The embedding of the query.
            top_k (int): The number of top results to return.

        Returns:
            dict: A dictionary containing the search results.
        """
        try:
            if top_k <= 0:
                logger.warning("top_k must be a positive integer. Received: %d", top_k)
                raise ValueError("top_k must be a positive integer.")
            
            query_kwargs = {
                "query_embeddings": [query_embedding],
                "n_results": top_k,
                "include": include,
            }

            if where is not None:
                query_kwargs["where"] = where

            if include is None:
                query_kwargs["include"] = ["documents", "metadatas", "distances"]

            logger.info("Searching the vector store with top_k=%d and where=%s.", top_k, where)
            results = self.collection.query(**query_kwargs)
            logger.info("Search completed. Found %d results.", len(results.get("ids", [])))
            return results
        except Exception as e:
            logger.exception("Failed to search records in the vector store: %s", str(e))
            raise RuntimeError("Failed to search records in the vector store.") from e

    def get_neighboring_chunks(
            self,
            chunk_index: int,
            transcript_id: str,
            user_id: str,
            neighbor_range: int = 1,
    ) -> dict:
        """
        Retrieves neighboring chunks based on the provided chunk index.

        Args:
        Args:
            chunk_index (int): The index of the current chunk.
            neighbor_range (int): The range of neighboring chunks to retrieve.
            transcript_id (UUID): The transcript ID of the current chunk.
            user_id (UUID): The user ID of the current chunk.
        Returns:
            dict: A dictionary containing the neighboring chunk records.
        """
        try:
            if neighbor_range < 1:
                logger.warning("neighbor_range must be a positive integer. Received: %d", neighbor_range)
                raise ValueError("neighbor_range must be a positive integer.")
            
            # IF chunk_index is 0, we can only get the next chunk   
            #otherwise, we can get the previous and next chunks
            start_index = max(0, chunk_index - neighbor_range)
            end_index = chunk_index + neighbor_range
            
            where_filter = {
                "$and": [
                    {"transcript_id": transcript_id},
                    {"user_id": user_id},
                    {"chunk_index": {"$gte": start_index}},
                    {"chunk_index": {"$lte": end_index}},
                ]
            }

            #logger.info("Retrieving neighboring chunks for chunk_index=%d with neighbor_range=%d.", chunk_index, neighbor_range)
            results = self.collection.get(
                where=where_filter,
                include=["documents", "metadatas"],
            )
            return results
        
        except Exception as e:
            logger.exception("Failed to retrieve neighboring chunks: %s", str(e))
            raise RuntimeError("Failed to retrieve neighboring chunks.") from e