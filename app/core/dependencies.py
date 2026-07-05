from fastapi import Depends

from app.repositories.postgres_todo_repository import PostgresTodoRepository
from app.services.todo_service import TodoService
from app.database.database import get_db


def get_postgres_repository(
    db=Depends(get_db),
):
    return PostgresTodoRepository(db)


def get_service(
    repository=Depends(get_postgres_repository),
):
    return TodoService(repository)

