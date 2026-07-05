from typing import Optional

from pydantic import BaseModel, EmailStr, Field

class SignUpRequest(BaseModel):
    """
    Schema for sign-up request data.
    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password, must be at least 8 characters long.
        name (str): The user's full name.
    """

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    name: str = Field(..., min_length=1, max_length=100)
    
class SignUpResponse(BaseModel):
    """
    Response schema for successful sign-up.
    Attributes:
        message (str): A message indicating the result of the sign-up operation.
        user_confirmed (bool): Indicates whether the user is confirmed.
    """
    message: str
    user_confirmed: bool

class ConfirmSignUpRequest(BaseModel):
    """
    Schema for confirm sign-up request data.
    Attributes:
        email (EmailStr): The user's email address.
        confirmation_code (str): The confirmation code sent to the user's email.
    """
    email: EmailStr
    confirmation_code: str = Field(..., pattern=r'^\d{6}$')  # Assuming confirmation code is 6 digits long

class ConfirmSignUpResponse(BaseModel):
    """
    Response schema for successful confirmation of sign-up.
    Attributes:
        message (str): A message indicating the result of the confirmation operation.
    """
    message: str
    
class LoginRequest(BaseModel):
    """
    Schema for login request data.
    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password, must be at least 8 characters long.
    """

    email: EmailStr
    password: str = Field(..., min_length=8)


class LoginResponse(BaseModel):
    """
    Response schema for successful login.
    """
    access_token: str
    id_token: str
    refresh_token: str
    expires_in: int
    token_type: str


class TokenClaims(BaseModel):
    """
    Schema for JWT token claims.
    Attributes:
        sub (str): The subject of the token, typically the user ID.
        iss (str): The issuer of the token.
        client_id (str): The client ID associated with the token.
        token_use (str): The intended use of the token (e.g., "access").
        username (str): The username associated with the token.
        exp (int): The expiration time of the token (in seconds since epoch).
        iat (int): The time at which the token was issued (in seconds since epoch).
        auth_time (int): The time at which the user authenticated (in seconds since epoch).
        scope (Optional[str]): The scope of access granted by the token.
        origin_jti (Optional[str]): The original JWT ID, if applicable.
        event_id (Optional[str]): An optional event ID associated with the token.
        jti (Optional[str]): The JWT ID, a unique identifier for the token.
    """
    sub: str
    iss: str
    client_id: str
    token_use: str
    username: str

    exp: int
    iat: int
    auth_time: int

    scope: Optional[str] = None
    origin_jti: Optional[str] = None
    event_id: Optional[str] = None
    jti: Optional[str] = None

class RefreshTokenRequest(BaseModel):
    """
    Schema for refresh token request data.
    Attributes:
        username (str): The username associated with the refresh token.
        refresh_token (str): The refresh token used to obtain a new access token.
    """
    username: str
    refresh_token: str

class RefreshTokenResponse(BaseModel):
    """
    Response schema for successful refresh token operation.
    Attributes:
        access_token (str): The new access token.
        id_token (str): The new ID token.
        expires_in (int): The expiration time of the new access token (in seconds).
        token_type (str): The type of the new token (e.g., "Bearer").
    """
    access_token: str
    id_token: str
    expires_in: int
    token_type: str

class SignOutRequest(BaseModel):
    """
    Schema for sign-out request data.
    Attributes:
        access_token (str): The access token of the user to sign out.
    """
    access_token: str

class SignOutResponse(BaseModel):
    """
    Response schema for successful sign-out operation.
    Attributes:
        message (str): A message indicating the result of the sign-out operation.
    """
    message: str