

import logging

from app.auth.schemas import TokenClaims
from app.schemas.user import UserCreate, CurrentUserResponse

logger = logging.getLogger(__name__)

class UserService:
    """
    Service responsible for handling business logic related to User items.
    """

    def __init__(self, user_repository):
        self.user_repository = user_repository
    
    def _to_response(self, model) -> CurrentUserResponse:
        """Convert a SQLAlchemy UserModel to a Pydantic CurrentUserResponse."""
        return CurrentUserResponse(
            id=model.id,
            cognito_sub=model.cognito_sub,
            username=model.username,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def get_user_by_cognito_sub(self, cognito_sub: str) -> CurrentUserResponse | None:
        """Retrieve a User item by its Cognito sub."""
        logger.debug(f"Looking up user by cognito_sub: {cognito_sub}")
        user = self.user_repository.get_by_cognito_sub(cognito_sub)
        if user is None:
            logger.warning(f"User not found for cognito_sub: {cognito_sub}")
            return None
        return self._to_response(user)
    
    def get_or_create_user(self, claims: TokenClaims) -> CurrentUserResponse:
        """
        Retrieve a User item by its Cognito sub, or create a new one if it doesn't exist.
        """
        cognito_sub = claims.sub
        logger.debug(f"get_or_create_user called for cognito_sub: {cognito_sub}")
        user = self.get_user_by_cognito_sub(cognito_sub)

        if user is None:
            logger.info(f"No existing user for cognito_sub: {cognito_sub}. Creating new record.")
            user_create = UserCreate(
                cognito_sub=cognito_sub,
                username=claims.username
            )
            user = self.create_user(user_create)

        return user

    def create_user(self, user_create: UserCreate) -> CurrentUserResponse:
        """Create a new User item."""
        logger.info(f"Creating user with cognito_sub: {user_create.cognito_sub}")
        user = self.user_repository.create(user_create)
        logger.info(f"User created successfully: {user.id}")
        return user

    def update_user(
            self,
            *,
            id:str,
            username:str) -> CurrentUserResponse:
        """Update an existing User item."""
        logger.info(f"Updating user: {id}")
        user = self.user_repository.update(id=id, username=username)
        logger.info(f"User updated successfully: {user.id}")
        return user

    def delete_user(
            self, 
            *,
            id: str) -> bool:
        """Delete a User item."""
        logger.info(f"Deleting user: {id}")
        result = self.user_repository.delete(id=id)
        if result:
            logger.info(f"User deleted successfully: {id}")
        else:
            logger.warning(f"Failed to delete user: {id}")
        return result