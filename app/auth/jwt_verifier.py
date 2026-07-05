import jwt
import requests
import json
import logging

from app.core.config import settings

class JWTVerifier:

    def __init__(self):
        """
        Initializes the JWTVerifier with the necessary configuration for verifying JWT tokens.
        """
        self.issuer =(
            f"https://cognito-idp.{settings.AWS_REGION}.amazonaws.com/{settings.COGNITO_USER_POOL_ID}"
        )
        self.jwks_url = f"{self.issuer}/.well-known/jwks.json"  
        self.client_id = settings.COGNITO_CLIENT_ID
        self.jwks = self._download_jwks()  # Download JWKS during initialization
        self.logger = logging.getLogger(__name__)

    def _get_signing_key(self, token: str):
        """
        Retrieves the public key used for verifying JWT tokens.

        Returns:
            str: The public key as a string.
        """
        
        header = jwt.get_unverified_header(token)

        #print("Header:", header)  # Debugging line to print the JWT header

        kid = header.get("kid")

        if not kid:
            raise ValueError("No 'kid' found in token header.")
        
        for key in self.jwks.get("keys", []):
            if key.get("kid") == kid:
                return key
            
        raise ValueError("Public key not found for the given 'kid'.")

    def _download_jwks(self) -> dict:
        """
        Downloads the JSON Web Key Set (JWKS) from the authorization server.

        Returns:
            dict: The JWKS containing public keys for token verification.
        """
        # Timeout prevents hanging the application on slow/unresponsive JWKS endpoint
        response = requests.get(self.jwks_url, timeout=5)
        response.raise_for_status()
        return response.json()

    def _decode_token(self, token: str, signing_key: str) -> dict:
        """
        Decodes the JWT using the provided public key.

        Args:
            token (str): The JWT to decode.
            signing_key (str): The public key used for decoding.

        Returns:
            dict: The decoded payload of the JWT.
        """
        # Implementation for decoding the JWT
        try:
            #convert JWK -> RSA public key
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(
                json.dumps(signing_key)
                )
            
            #Decode JWT
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                issuer=self.issuer,
            )
            #print("Decoded Payload:", payload)  # Debugging line to print the decoded payload
            #Veriy token_use
            issuer = self.issuer
            if payload.get("iss") != issuer:
                raise ValueError("Invalid issuer.")
            
            #Verify Client_id
            if payload.get("client_id") != self.client_id:
                raise ValueError("Invalid client_id.")
            
            if payload.get("token_use") != "access":
                raise ValueError("Invalid token_use. Expected 'access'.")
            
            #Return Claims
            return payload
        
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired.")
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Invalid token: {str(e)}")
        
    def verify_access_token(self, token: str) -> dict:
        """
        Verifies the provided access token and returns the decoded payload.
        """
        try:
            signing_key = self._get_signing_key(token)
            payload = self._decode_token(token, signing_key)
            self.logger.info("Access token verified successfully for sub: %s", payload.get("sub"))
            return payload
        except ValueError as e:
            self.logger.warning("Access token verification failed: %s", str(e))
            raise
        except Exception as e:
            self.logger.error("Unexpected error during token verification: %s", str(e))
            raise
        

