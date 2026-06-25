from fastapi import APIRouter, Depends, status
from fastapi.responses import Response
from uuid import UUID

from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate
from app.services.todo_service import TodoService
from app.core.dependencies import get_service

router = APIRouter()

@router.get(
        "/todos",
        response_model=list[TodoResponse],
        status_code=200,  # 200 OK is the correct HTTP status code for a successful GET request.
        )
def get_todos(
    service: TodoService = Depends(get_service)
):
    """
    Get all Todos.
    """
    return service.get_all()

@router.post(
        "/todos",
        response_model=TodoResponse,
        status_code=201,   #201 Created is the correct HTTP status code when a new resource is successfully created.
        )
def create_todo(todo: TodoCreate, service: TodoService = Depends(get_service)):
    """
    Create a new Todo.
    """
    return service.create(todo)          

@router.get(
        "/todos/{todo_id}",
        response_model=TodoResponse,
        status_code=200,  # 200 OK is the correct HTTP status code for a successful GET request.
        )
def get_todo_by_id(todo_id: UUID, service: TodoService = Depends(get_service)):
    """
    Get a Todo by its ID.
    """
    return service.get_by_id(todo_id)

@router.put(
        "/todos/{todo_id}",
        response_model=TodoResponse,
        status_code=200,  # 200 OK is the correct HTTP status code for a successful PUT request.
        )
def update_todo(todo_id: UUID, todo_update: TodoUpdate, service: TodoService = Depends(get_service)):
    """
    Update an existing Todo.
    """
    return service.update(todo_id, todo_update)

@router.delete(
        "/todos/{todo_id}",
        status_code=status.HTTP_204_NO_CONTENT,  # 204 No Content is the correct HTTP status code when a resource is successfully deleted.
        )
def delete_todo(todo_id: UUID, service: TodoService = Depends(get_service)):
    """
    Delete a Todo by its ID.
    """
    service.delete(todo_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
