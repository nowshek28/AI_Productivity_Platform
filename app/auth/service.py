from app.auth.cognito import CognitoClient
from app.auth.jwt_verifier import JWTVerifier
from app.auth.schemas import ConfirmSignUpResponse, LoginResponse, RefreshTokenResponse, SignOutResponse, SignUpResponse

class AuthService:

    def __init__(
            self,
            cognito_client: CognitoClient,
            jwt_verifier: JWTVerifier,
            ):
        """
        Initialize the AuthService with a Cognito client and JWT verifier.
        """
        self.cognito_client = cognito_client
        self.jwt_verifier = jwt_verifier

    def sign_up(self, email: str, password: str, name: str) -> SignUpResponse:
        """
        Sign up a new user using their email and password.
        Args:
            email (str): The user's email address.
            password (str): The user's password.
            name (str): The user's full name.
            
        Returns:
            SignUpResponse
        """
        response = self.cognito_client.sign_up(email=email, password=password, name=name)
        return SignUpResponse(
            message="User signed up successfully.",
            user_confirmed=response.get("UserConfirmed", False)
        )
    
    def confirm_sign_up(self, email: str, confirmation_code: str) -> ConfirmSignUpResponse:
        """
        Confirm a user's sign-up using their email and confirmation code.
        Args:
            email (str): The user's email address.
            confirmation_code (str): The confirmation code sent to the user's email.
    
        Returns:
            ConfirmSignUpResponse
        """
        response = self.cognito_client.confirm_sign_up(email=email, confirmation_code=confirmation_code)
        return response

    def login(self, email: str, password: str) -> LoginResponse:
        """
        Authenticate a user using their email and password.
        Args:
            email (str): The user's email address.
            password (str): The user's password.
            
        Returns:
            LoginResponse
        """

        response = self.cognito_client.login(
            username=email, 
            password=password
            )
        
        authentication_response = response['AuthenticationResult']

        return LoginResponse(
            access_token=authentication_response['AccessToken'],
            refresh_token=authentication_response['RefreshToken'],
            id_token=authentication_response['IdToken'],
            expires_in=authentication_response['ExpiresIn'],
            token_type=authentication_response['TokenType']
        )
    
    def verify_access_token(self, token: str) -> dict:
        """
        Verify a JWT token.
        Args:
            token (str): The JWT token to verify.
            
        Returns:
            dict: The decoded payload of the JWT if verification is successful.
        """
        return self.jwt_verifier.verify_access_token(token)
    
    def refresh_access_token(self, username: str, refresh_token: str) -> RefreshTokenResponse:
        """
        Refresh the access token using a refresh token.
        Args:
            username (str): The username associated with the refresh token.
            refresh_token (str): The refresh token to use for obtaining a new access token.
            
        Returns:
            RefreshTokenResponse
        """
        response = self.cognito_client.refresh_access_token(username=username, refresh_token=refresh_token)
        return response
    
    def global_sign_out(self, access_token: str) -> SignOutResponse:
        """
        Sign out a user globally, invalidating all their sessions.
        Args:
            access_token (str): The access token of the user to sign out.
        """
        return self.cognito_client.global_sign_out(access_token=access_token)
