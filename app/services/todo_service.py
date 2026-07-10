from datetime import datetime, timezone
from uuid import UUID, uuid4
import logging

from app.schemas.todo import ToDoPriority, ToDoCategory, TodoCreate, TodoResponse, TodoUpdate
from app.exceptions.todo import TodoNotFoundError

logger = logging.getLogger(__name__)

class TodoService:
    """
    Service responsible for Todo business logic.
    """
    def __init__(self, repository):
        self.repository = repository

    def _to_response(self, model) -> TodoResponse:
        """
        Convert a TodoModel to a TodoResponse.
        """
        return TodoResponse(
            id=model.id,
            title=model.title,
            description=model.description,
            completed=model.completed,
            user_id=model.user_id,
            priority=model.priority,
            category=model.category,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    
    def create(self, todo: TodoCreate, user_id: str) -> TodoResponse:
        """
        Create a new Todo.
        """
        logger.info(f"Creating a new todo for user {user_id}.")

        new_todo = self.repository.create(
            title=todo.title,
            description=todo.description,
            user_id=user_id,
            priority=todo.priority,
            category=todo.category,
        )

        logger.info(f"Todo created successfully: {new_todo.id}")
        return self._to_response(new_todo)
    
    def get_all(self, user_id: str) -> list[TodoResponse]:
        """
        Retrieve all Todos for the given user.
        """
        todos = self.repository.get_all(user_id=user_id)
        logger.info(f"Retrieved {len(todos)} todos for user {user_id}.")
        return [self._to_response(todo) for todo in todos]
    
    def get_by_id(self, todo_id: UUID, user_id: str) -> TodoResponse:
        """
        Retrieve a Todo by its ID, scoped to the given user.
        """
        todo = self.repository.get_by_id(todo_id, user_id=user_id)

        if todo is None:
            logger.warning(f"Todo {todo_id} not found for user {user_id}")
            raise TodoNotFoundError(todo_id)
        logger.info(f"Todo {todo_id} retrieved successfully.")
        return self._to_response(todo)
    
    def get_by_completed(self, completed: bool, user_id: str) -> list[TodoResponse]:
        """
        Retrieve all Todos for the given user with a specific completed status.
        """
        todos = self.repository.get_by_completed(completed=completed, user_id=user_id)
        logger.info(f"Retrieved {len(todos)} todos for user {user_id} with completed={completed}.")
        return [self._to_response(todo) for todo in todos]
    
    def get_by_priority(self, priority: ToDoPriority, user_id: str) -> list[TodoResponse]:
        """
        Retrieve all Todos for the given user with a specific priority.
        """
        todos = self.repository.get_by_priority(priority=priority, user_id=user_id)
        logger.info(f"Retrieved {len(todos)} todos for user {user_id} with priority={priority}.")
        return [self._to_response(todo) for todo in todos]
    
    def get_by_category(self, category: ToDoCategory, user_id: str) -> list[TodoResponse]:
        """
        Retrieve all Todos for the given user with a specific category.
        """
        todos = self.repository.get_by_category(category=category, user_id=user_id)
        logger.info(f"Retrieved {len(todos)} todos for user {user_id} with category={category}.")
        return [self._to_response(todo) for todo in todos]

    def update(self, todo_id: UUID, todo_update: TodoUpdate, user_id: str) -> TodoResponse:
        """
        Update an existing Todo, scoped to the given user.
        """
        existing_todo = self.repository.get_by_id(todo_id, user_id=user_id)

        if existing_todo is None:
            logger.warning(f"Todo {todo_id} not found for user {user_id}")
            raise TodoNotFoundError(todo_id)

        updated_todo = TodoUpdate(
            title=todo_update.title if todo_update.title != "string" else existing_todo.title,
            description=todo_update.description if todo_update.description != "string" else existing_todo.description,
            completed=todo_update.completed if todo_update.completed is not None else existing_todo.completed,
            priority=todo_update.priority if todo_update.priority != "string" else existing_todo.priority,
            category=todo_update.category if todo_update.category != "string" else existing_todo.category,   
        )
        logger.info(f"Todo {todo_id} updated successfully.")
        updated_todo = self.repository.update(
            todo_id=todo_id,
            title=updated_todo.title,
            description=updated_todo.description,
            completed=updated_todo.completed,
            priority=updated_todo.priority,
            category=updated_todo.category,
            updated_at=datetime.now(timezone.utc),
            user_id=user_id
            )
        return self._to_response(updated_todo)
    
    def delete(self, todo_id: UUID, user_id: str) -> bool:
        """
        Delete a Todo by its ID, scoped to the given user.
        """
        existing_todo = self.repository.get_by_id(todo_id, user_id=user_id)

        if existing_todo is None:
            logger.warning(f"Todo {todo_id} not found for user {user_id}")
            raise TodoNotFoundError(todo_id)
        logger.info(f"Todo {todo_id} deleted successfully.")

        return self.repository.delete(todo_id, user_id=user_id)


