from app.auth.exceptions import InvalidCredentialsError, NotAuthorizedError, UserNotConfirmedError
from app.auth.schemas import ConfirmSignUpResponse, RefreshTokenResponse, SignOutResponse
from app.schemas.todo import TodoResponse


class FakeJWTVerifier:
    """
    In-memory JWT verifier for tests — no crypto, no network.
    Any token equal to VALID_TOKEN is accepted; all others raise ValueError.
    """
    VALID_TOKEN = "fake-access-token"
    FAKE_CLAIMS = {
        "sub": "fake-user-sub-uuid",
        "iss": "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_FAKEPOOL",
        "client_id": "fake-client-id",
        "token_use": "access",
        "username": "test@example.com",
        "exp": 9999999999,
        "iat": 1000000000,
        "auth_time": 1000000000,
    }

    def verify_access_token(self, token: str) -> dict:
        if token != self.VALID_TOKEN:
            raise ValueError("Invalid token.")
        return self.FAKE_CLAIMS


class FakeCognitoClient:
    """
    In-memory Cognito stand-in for unit/integration tests.
    No AWS credentials or network access required.
    """

    VALID_CONFIRMATION_CODE = "123456"

    def __init__(self):
        # email -> {password, name, confirmed}
        self._users: dict = {}

    def sign_up(self, email: str, password: str, name: str) -> dict:
        if email in self._users:
            raise InvalidCredentialsError("User already exists.")
        self._users[email] = {"password": password, "name": name, "confirmed": False}
        return {"UserConfirmed": False, "UserSub": "fake-user-sub-uuid"}

    def confirm_sign_up(self, email: str, confirmation_code: str) -> ConfirmSignUpResponse:
        if email not in self._users:
            raise InvalidCredentialsError("User not found.")
        if confirmation_code != self.VALID_CONFIRMATION_CODE:
            raise InvalidCredentialsError("Invalid confirmation code.")
        self._users[email]["confirmed"] = True
        return ConfirmSignUpResponse(message="User confirmed successfully.")

    def login(self, username: str, password: str) -> dict:
        user = self._users.get(username)
        if user is None or user["password"] != password:
            raise InvalidCredentialsError("Invalid username or password.")
        if not user["confirmed"]:
            raise UserNotConfirmedError("User is not confirmed.")
        return {
            "AuthenticationResult": {
                "AccessToken": "fake-access-token",
                "IdToken": "fake-id-token",
                "RefreshToken": "fake-refresh-token",
                "ExpiresIn": 3600,
                "TokenType": "Bearer",
            }
        }

    def refresh_access_token(self, username: str, refresh_token: str) -> RefreshTokenResponse:
        if username not in self._users or refresh_token != "fake-refresh-token":
            raise NotAuthorizedError("Invalid refresh token.")
        return RefreshTokenResponse(
            access_token="fake-new-access-token",
            id_token="fake-new-id-token",
            expires_in=3600,
            token_type="Bearer",
        )

    def global_sign_out(self, access_token: str) -> SignOutResponse:
        if access_token != "fake-access-token":
            raise NotAuthorizedError("Invalid access token.")
        return SignOutResponse(message="User signed out globally successfully.")


class FakeTodoRepository:

    def __init__(self):
        self.todos = []

    def create(self, todo: TodoResponse):
        self.todos.append(todo)
        return todo

    def get_all(self):
        return self.todos

    def get_by_id(self, todo_id):
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def update(self, todo_id, updated_todo):
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                self.todos[i] = updated_todo
                return updated_todo
        return None

    def delete(self, todo_id):
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                del self.todos[i]
                return True
        return False