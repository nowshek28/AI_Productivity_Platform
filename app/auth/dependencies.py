from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.cognito import CognitoClient
from app.auth.jwt_verifier import JWTVerifier
from app.auth.schemas import TokenClaims
from app.auth.service import AuthService

security = HTTPBearer()

def get_cognito_client() -> CognitoClient:
    """
    Dependency to get an instance of CognitoClient.
    """
    return CognitoClient()

def get_jwt_verifier() -> JWTVerifier:
    return JWTVerifier()

def get_auth_service(cognito_client: CognitoClient = Depends(get_cognito_client),
                     jwt_verifier: JWTVerifier = Depends(get_jwt_verifier)) -> AuthService:
    """
    Dependency to get an instance of AuthService.
    """
    return AuthService(cognito_client, jwt_verifier)

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        verifier: JWTVerifier = Depends(get_jwt_verifier),
) -> TokenClaims:
    """
    Dependency to get the current authenticated user based on the provided JWT token.
    Args:
        credentials (HTTPAuthorizationCredentials): The HTTP authorization credentials containing the JWT token.
        verifier (JWTVerifier): The JWT verifier instance to decode and verify the token.
        
    Returns:
        TokenClaims: The decoded claims from the JWT token.
    """
    token = credentials.credentials
    claims = verifier.verify_access_token(token)
    return TokenClaims(**claims)