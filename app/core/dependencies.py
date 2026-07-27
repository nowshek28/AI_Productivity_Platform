from fastapi import Depends

from app.repositories.postgres_todo_repository import PostgresTodoRepository
from app.repositories.postgres_user_repository import PostgresUserRepository
from app.repositories.transcript_repository import TranscriptRepository
from app.repositories.session_repository import SessionRepository
from app.repositories.chatmessage_repository import ChatMessageRepository

from app.services.todo_service import TodoService
from app.services.transcript_service import TranscriptService
from app.services.user_service import UserService
from app.services.storage_service import StorageService
from app.services.etl.etl_service import ETLService
from app.services.retrieval.retrieval_service import RetrievalService
from app.services.session.session_service import SessionService
from app.services.session.chatmessage_service import ChatMessageService
from app.services.reranking.cross_encoder_service import CrossEncoderService
from app.services.embeddings.embedding_service import EmbeddingService
from app.services.vector_store.vectorstore_service import VectorStoreService
from app.services.llm.llm_service import LLMService

from app.database.database import get_db
from app.database.chroma import transcript_collection, chroma_client


def get_postgres_repository(
    db=Depends(get_db),
):
    return PostgresTodoRepository(db)


def get_service(
    repository=Depends(get_postgres_repository),
):
    return TodoService(repository)

def get_user_repository(
    db=Depends(get_db),
):
    return PostgresUserRepository(db)

def get_user_service(
    repository=Depends(get_user_repository),
):
    return UserService(repository)

def get_transcript_repository(
    db=Depends(get_db),
):
    return TranscriptRepository(db)

def get_s3_storage_service():
    return StorageService()

def get_etl_service():
    return ETLService()

def get_transcript_service(
    transcript_repository=Depends(get_transcript_repository),
    todo_repository=Depends(get_postgres_repository),
    storage_service=Depends(get_s3_storage_service),
    etl_service=Depends(get_etl_service),
):
    return TranscriptService(transcript_repository, todo_repository, storage_service, etl_service)

embedding_service = EmbeddingService()
cross_encoder_service = CrossEncoderService()
vector_store_service = VectorStoreService()
llm_service = LLMService()

def get_embedding_service():
    return embedding_service


def get_cross_encoder_service():
    return cross_encoder_service


def get_vector_store_service():
    return vector_store_service


def get_llm_service():
    return llm_service

def get_retrieval_service(
    embedding_service=Depends(get_embedding_service),
    vector_store_service=Depends(get_vector_store_service),
    cross_encoder_service=Depends(get_cross_encoder_service),
    llm_service=Depends(get_llm_service)
):
    return RetrievalService(
        embedding_service=embedding_service,
        vector_store=vector_store_service,
        cross_encoder_service=cross_encoder_service,
        llm_service=llm_service,
    )

def get_chroma_client():
    return chroma_client

def get_transcript_collection():
    return transcript_collection

def get_session_repository(
    db=Depends(get_db),
):
    return SessionRepository(db)

def get_session_service(
    session_repository=Depends(get_session_repository),
    transcript_repository=Depends(get_transcript_repository),
):
    return SessionService(session_repository, transcript_repository)

def get_chat_message_repository(
    db=Depends(get_db),
):
    return ChatMessageRepository(db)

def get_chat_message_service(
    chat_message_repository=Depends(get_chat_message_repository),
):
    return ChatMessageService(chat_message_repository)