class AuthenticationError(Exception):
    """Exception raised for authentication errors."""
    pass

class UserAlreadyExistsError(Exception):
    """Exception raised when a user already exists during sign-up."""
    pass

class UserNotConfirmedError(Exception):
    """Exception raised when a user is not confirmed during login."""
    pass

class InvalidCredentialsError(Exception):
    """Exception raised for invalid login credentials."""
    pass

class UserNotFoundError(Exception):
    """Exception raised when a user is not found."""
    pass

class NotAuthorizedError(Exception):
    """Exception raised when a user is not authorized to perform an action."""
    pass