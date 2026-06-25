from datetime import datetime, timezone
from uuid import UUID, uuid4
import logging

from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate
from app.exceptions.todo import TodoNotFoundError
from app.repositories.todo_repository import TodoRepository

logger = logging.getLogger(__name__)

class TodoService:
    """
    Service responsible for Todo business logic.
    """
    def __init__(self, repository:TodoRepository):
        self.repository = repository

    def create(self, todo: TodoCreate) -> TodoResponse:
        """
        Create a new Todo.
        """
        logger.info(f"Creating a new todo.")
        now = datetime.now(timezone.utc)

        new_todo = TodoResponse(
            id=uuid4(),
            title=todo.title,
            description=todo.description,
            completed=False,
            created_at=now,
            updated_at=now,
        )

        logger.info(f"Todo created successfully: {new_todo.id}")
        return self.repository.create(new_todo)
    
    def get_all(self) -> list[TodoResponse]:
        """
        Retrieve all Todos.
        """
        todos = self.repository.get_all()
        logger.info(f"Retrieved {len(todos)} todos.")
        return todos
    
    def get_by_id(self, todo_id: UUID) -> TodoResponse | None:
        """
        Retrieve a Todo by its ID.
        """
        todo = self.repository.get_by_id(todo_id)

        if todo is None:
            logger.warning(f"Todo {todo_id} not found")
            raise TodoNotFoundError(todo_id)
        logger.info(f"Todo {todo_id} retrieved successfully.")
        return todo
    
    def update(self, todo_id: UUID, todo_update: TodoUpdate) -> TodoResponse | None:
        """
        Update an existing Todo.
        """
        existing_todo = self.repository.get_by_id(todo_id)

        if existing_todo is None:
            logger.warning(f"Todo {todo_id} not found")
            raise TodoNotFoundError(todo_id)

        updated_todo = existing_todo.model_copy(
            update=todo_update.model_dump(exclude_unset=True)
            )
        updated_todo.updated_at = datetime.now(timezone.utc)
        logger.info(f"Todo {todo_id} updated successfully.")
        return self.repository.update(todo_id, updated_todo)
    
    def delete(self, todo_id: UUID) -> bool:
        """
        Delete a Todo by its ID.
        """
        existing_todo = self.repository.get_by_id(todo_id)

        if existing_todo is None:
            logger.warning(f"Todo {todo_id} not found")
            raise TodoNotFoundError(todo_id)
        logger.info(f"Todo {todo_id} deleted successfully.")

        return self.repository.delete(todo_id)


