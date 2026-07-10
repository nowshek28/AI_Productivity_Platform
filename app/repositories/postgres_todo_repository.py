from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.database.models import TodoModel


class PostgresTodoRepository:
    """
    Repository responsible for storing and retrieving Todo items in a PostgreSQL database.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, user_id: str) -> list[TodoModel]:
        """Retrieve all Todo items for a specific user from the database."""
        models = self.db.query(TodoModel).filter(TodoModel.user_id == user_id).all()
        return models

    def get_by_id(self, todo_id: UUID, user_id: str) -> TodoModel | None:
        """Retrieve a Todo item by its ID from the database."""
        model = self.db.query(TodoModel).filter(TodoModel.id == str(todo_id), TodoModel.user_id == user_id).first()
        if model is None:
            return None
        return model
    
    def get_by_completed(self, completed: bool, user_id: str) -> list[TodoModel]:
        """Retrieve all Todo items for a specific user with a specific completed status from the database."""
        models = self.db.query(TodoModel).filter(TodoModel.completed == completed, TodoModel.user_id == user_id).all()
        return models
    
    def get_by_priority(self, priority: str, user_id: str) -> list[TodoModel]:
        """Retrieve all Todo items for a specific user with a specific priority from the database.
        IF response is empty, call TodoResponseValidationError exception handler to return a 422 error with a message indicating that the priority is invalid."""
        models = self.db.query(TodoModel).filter(TodoModel.priority == priority, TodoModel.user_id == user_id).all()
        return models
    
    def get_by_category(self, category: str, user_id: str) -> list[TodoModel]:
        """Retrieve all Todo items for a specific user with a specific category from the database.
        IF response is empty, call TodoResponseValidationError exception handler to return a 422 error with a message indicating that the category is invalid."""
        models = self.db.query(TodoModel).filter(TodoModel.category == category, TodoModel.user_id == user_id).all()
        return models   

    def create(
            self,
            *,
            title: str,
            description: str,
            user_id: str,
            priority: str,
            category: str,
    ) -> TodoModel:
        """Create a new Todo item in the database."""
        new_model = TodoModel(
            title=title,
            description=description,
            user_id=user_id,
            priority=priority,
            category=category,
        )
        self.db.add(new_model)
        self.db.commit()
        self.db.refresh(new_model)
        return new_model

    def update(
            self,
            *,
            todo_id: UUID,
            title: str,
            description: str,
            completed: bool,
            priority: str,
            category: str,
            updated_at: datetime,
            user_id: str
    ) -> TodoModel | None:
        """Update an existing Todo item in the database."""
        model = self.db.query(TodoModel).filter(TodoModel.id == str(todo_id), TodoModel.user_id == user_id).first()
        if not model:
            return None
        
        # Check if the title, description, or completed status has changed before updating
        if (model.title == title and
            model.description == description and
            model.completed == completed and
            model.priority == priority and
            model.category == category
        ):
            return model  # No changes, return the existing model
        
        # Update the fields only if they title is not "string" and the description is not "string"
        if model.title != title and title != "string":
            model.title = title

        if model.description != description and description != "string":
            model.description = description

        if model.completed != completed:
            model.completed = completed

        if model.priority != priority:
            model.priority = priority

        if model.category != category:
            model.category = category

        model.updated_at = updated_at

        self.db.commit()
        self.db.refresh(model)
        return model

    def delete(self, todo_id: UUID, user_id: str) -> bool:
        """Delete a Todo item by its ID from the database."""
        model = self.db.query(TodoModel).filter(TodoModel.id == str(todo_id), TodoModel.user_id == user_id).first()
        if not model:
            return False
        self.db.delete(model)
        self.db.commit()
        return True


