from uuid import UUID

from sqlalchemy.orm import Session

from app.database.models import TodoModel
from app.schemas.todo import TodoResponse


class PostgresTodoRepository:
    """
    Repository responsible for storing and retrieving Todo items in a PostgreSQL database.
    """

    def __init__(self, db: Session):
        self.db = db

    def _to_response(self, model: TodoModel) -> TodoResponse:
        """Convert a SQLAlchemy TodoModel to a Pydantic TodoResponse."""
        return TodoResponse(
            id=model.id,
            title=model.title,
            description=model.description,
            completed=model.completed,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def get_all(self) -> list[TodoResponse]:
        """Retrieve all Todo items from the database."""
        models = self.db.query(TodoModel).all()
        return [self._to_response(m) for m in models]

    def get_by_id(self, todo_id: UUID) -> TodoResponse | None:
        """Retrieve a Todo item by its ID from the database."""
        model = self.db.query(TodoModel).filter(TodoModel.id == str(todo_id)).first()
        if model is None:
            return None
        return self._to_response(model)

    def create(self, todo: TodoResponse) -> TodoResponse:
        """Create a new Todo item in the database."""
        new_model = TodoModel(
            id=str(todo.id),
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
        )
        self.db.add(new_model)
        self.db.commit()
        self.db.refresh(new_model)
        return self._to_response(new_model)

    def update(self, todo_id: UUID, updated_todo: TodoResponse) -> TodoResponse | None:
        """Update an existing Todo item in the database."""
        model = self.db.query(TodoModel).filter(TodoModel.id == str(todo_id)).first()
        if not model:
            return None
        
        # Check if the title, description, or completed status has changed before updating
        if (model.title == updated_todo.title and
            model.description == updated_todo.description and
            model.completed == updated_todo.completed
        ):
            return self._to_response(model)  # No changes, return the existing model
        
        # Update the fields only if they have changed
        if model.title != updated_todo.title:
            model.title = updated_todo.title

        if model.description != updated_todo.description:
            model.description = updated_todo.description

        if model.completed != updated_todo.completed:
            model.completed = updated_todo.completed


        model.updated_at = updated_todo.updated_at

        self.db.commit()
        self.db.refresh(model)
        return self._to_response(model)

    def delete(self, todo_id: UUID) -> bool:
        """Delete a Todo item by its ID from the database."""
        model = self.db.query(TodoModel).filter(TodoModel.id == str(todo_id)).first()
        if not model:
            return False
        self.db.delete(model)
        self.db.commit()
        return True
