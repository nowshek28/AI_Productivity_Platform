from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.dependencies import get_auth_service
from app.auth.exceptions import InvalidCredentialsError, NotAuthorizedError, UserNotConfirmedError, UserNotFoundError
from app.auth.jwt_verifier import JWTVerifier
from app.auth.schemas import ConfirmSignUpResponse, ConfirmSignUpRequest, LoginRequest, LoginResponse, SignOutRequest, SignOutResponse, TokenClaims
from app.auth.schemas import SignUpRequest, SignUpResponse, RefreshTokenRequest, RefreshTokenResponse
from app.auth.service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

security = HTTPBearer()

@router.post(
    "/signup",
    response_model=SignUpResponse,
    summary="Register a new user using AWS Cognito",
    response_description="Returns a message indicating the result of the sign-up operation"
)
def sign_up(
    sign_up_request: SignUpRequest,
    auth_service: AuthService = Depends(get_auth_service)
) -> SignUpResponse:
    """
    Register a new user using their email and password.
    
    Args:
        sign_up_request (SignUpRequest): The sign-up request containing email, password, and full name.
        auth_service (AuthService): The authentication service dependency.
        
    Returns:
        SignUpResponse: The response indicating the result of the sign-up operation.
    """
    # Always return the same response to prevent user enumeration
    try:
        return auth_service.sign_up(
            email=sign_up_request.email, 
            password=sign_up_request.password,
            name=sign_up_request.name
        )
    except InvalidCredentialsError as e:
        error_msg = str(e)
        if "already exists" in error_msg:
            # Return same shape as success to prevent email enumeration
            return SignUpResponse(message="If this email is not registered, a confirmation email has been sent.", user_confirmed=False)
        raise HTTPException(
            status_code=400,
            detail="Sign-up failed. Please check your input and try again."
        )
    

@router.post(
    "/confirm-signup",
    response_model=ConfirmSignUpResponse,
    summary="Confirm a user's sign-up using AWS Cognito",
    response_description="Returns a message indicating the result of the confirmation operation"
)
def confirm_sign_up(
    confirm_sign_up_request: ConfirmSignUpRequest,
    auth_service: AuthService = Depends(get_auth_service)
) -> ConfirmSignUpResponse:
    """
    Confirm a user's sign-up using their email and confirmation code.
    
    Args:
        confirm_sign_up_request (ConfirmSignUpRequest): The confirmation request containing email and confirmation code.
        auth_service (AuthService): The authentication service dependency.
        
    Returns:
        ConfirmSignUpResponse: The response indicating the result of the confirmation operation.
    """
    try:
        return auth_service.confirm_sign_up(
            email=confirm_sign_up_request.email, 
            confirmation_code=confirm_sign_up_request.confirmation_code
        )
    
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=400, 
            detail="Invalid confirmation code."
        )
    except UserNotConfirmedError:
        raise HTTPException(
            status_code=403, 
            detail="User account is not confirmed. Please check your email for confirmation instructions."
        )


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="authenticate user using AWS Cognito",
    response_description="Returns the authentication tokens upon successful login"
)
def login(
    login_request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
) -> LoginResponse:
    """
    Authenticate a user using their email and password.
    
    Args:
        login_request (LoginRequest): The login request containing email and password.
        auth_service (AuthService): The authentication service dependency.
        
    Returns:
        LoginResponse: The response containing authentication tokens.
    """

    try:
        return auth_service.login(
            email=login_request.email, 
            password=login_request.password
            )
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=401, 
            detail="Invalid email or password."
            )
    except UserNotConfirmedError:
        raise HTTPException(
            status_code=403, 
            detail="User account is not confirmed. Please check your email for confirmation instructions."
            )
    
    
@router.get(
    "/verify-token",
    response_model=TokenClaims,
    summary="Verify a JWT token",
    response_description="Returns the decoded payload of the JWT if verification is successful"
)
def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> TokenClaims:
    """
    Verify a JWT token.
    
    Args:
        credentials (HTTPAuthorizationCredentials): The HTTP authorization credentials containing the JWT token.
        auth_service (AuthService): The authentication service dependency.
        
    Returns:
        TokenClaims: The response containing the decoded payload of the JWT if verification is successful.
    """
    token = credentials.credentials
    try:
        payload = auth_service.verify_access_token(token)
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=401, 
            detail="Token verification failed."
        )
    

@router.post(
    "/refresh-token",
    response_model=RefreshTokenResponse,
    summary="Refresh the access token using a refresh token",
    response_description="Returns new authentication tokens upon successful refresh"
)
def refresh_token(
    refresh_token_request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
) -> RefreshTokenResponse:
    """
    Refresh the access token using a refresh token.
    
    Args:
        refresh_token_request (RefreshTokenRequest): The request containing the refresh token.
        auth_service (AuthService): The authentication service dependency.
        
    Returns:
        RefreshTokenResponse: The response containing new authentication tokens.
    """
    try:
        return auth_service.refresh_access_token(username=refresh_token_request.username, refresh_token=refresh_token_request.refresh_token)
    except NotAuthorizedError:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token."
        )


@router.post(
    "/global-sign-out",
    response_model=SignOutResponse,
    summary="Sign out a user globally, invalidating all their sessions",
    response_description="Returns a message indicating the result of the global sign-out operation"
)
def global_sign_out(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> SignOutResponse:
    """
    Sign out a user globally, invalidating all their sessions.
    
    Args:
        credentials (HTTPAuthorizationCredentials): The HTTP authorization credentials containing the access token.
        auth_service (AuthService): The authentication service dependency.
        
    Returns:
        SignOutResponse: The response indicating the result of the global sign-out operation.
    """
    access_token = credentials.credentials
    try:
        return auth_service.global_sign_out(access_token=access_token)
    except NotAuthorizedError:
        raise HTTPException(
            status_code=401,
            detail="Invalid access token."
        )
    except UserNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )