from fastapi import Depends

from app.storage.json_storage import json_storage
from app.repositories.todo_repository import TodoRepository
from app.services.todo_service import TodoService


def get_storage():
    return json_storage


def get_repository(
    storage=Depends(get_storage),
):
    return TodoRepository(storage)


def get_service(
    repository=Depends(get_repository),
):
    return TodoService(repository)