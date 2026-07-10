from sqlalchemy.orm import Session

from app.database.models import UserModel

class PostgresUserRepository:
    """
    Repository responsible for storing and retrieving User items in a PostgreSQL database.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_cognito_sub(self, cognito_sub: str) -> UserModel | None:
        """Retrieve a User item by its Cognito sub from the database."""
        model = (self.db.query(UserModel)
                .filter(UserModel.cognito_sub == cognito_sub)
                .first()
                )
        if model:
            return model
        return None

    def create(
            self,
            *,
            cognito_sub:str,
            username:str
            ) -> UserModel:
        """Create a new User item in the database."""
        new_user = UserModel(
            cognito_sub=cognito_sub,
            username=username
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    def update(self, user: UserModel) -> UserModel:
        """Update an existing User item in the database."""
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user: UserModel) -> bool:
        """Delete a User item from the database."""
        self.db.delete(user)
        self.db.commit()
        return True