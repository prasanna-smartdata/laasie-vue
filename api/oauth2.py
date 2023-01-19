from datetime import datetime, timedelta, timezone
from typing import Optional
from flask import request as flask_request
import jwt
from api import env_config
from api.app_logger import get_logger

logger = get_logger("oauth2")


class InvalidTokenResponse(Exception):
    """
    Indicates that the refresh token is invalid.
    """

    message: str

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.message = message


class VerificationException(Exception):
    """
    Represents the exception that occurs when a signed JWT fails verification.
    """

    message: str

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.message = message


class InvalidRequestException(Exception):
    """
    An exception that is returned when required parameters are missing.
    """

    message: str

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.message = message


class AuthorizationParamsException(Exception):
    """
    An exception that is returned if the authorization params cannot
    be constructed due to invalid/missing environment configuration.
    """

    message: str

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.message = message


def pre_oauth2_callback():
    """
    Validates the request by checking for:
    - error query-param
    - code is non-empty
    - state is non-empty and passes verification
    Raises InvalidRequestException if any of the above fails.
    """
    if env_config.JWT_SECRET is None:
        logger.error(
            "JWT_SECRET is empty! Cannot validate OAuth2 callback requests. Failing the request..."
        )
        raise InvalidRequestException(
            "Internal server error. Please contact the system administrator."
        )

    if "error" in flask_request.args:
        decoded = flask_request.query_string.decode()
        logger.error("Authorization server returned an error: %s", decoded)
        raise InvalidRequestException(decoded)

    try:
        encoded_state_jwt = flask_request.args.get("state")
        verify_state_jwt(encoded_state_jwt, env_config.JWT_SECRET)
    except VerificationException as ex:
        raise InvalidRequestException(ex.message) from ex

    if "code" not in flask_request.args:
        raise InvalidRequestException("code is required")


def get_encoded_state_jwt(secret: str) -> str:
    """
    Returns a JWT string with a 10 minute expiration.
    """
    return jwt.encode(
        {
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=10),
        },
        secret,
        algorithm="HS256",
    )


def verify_state_jwt(encoded_state_jwt: Optional[str], secret: str):
    """
    Verifies that the provided JWT decodes successfully.
    """
    if encoded_state_jwt is None:
        raise VerificationException("Invalid request. Missing state query-param.")

    try:
        jwt.decode(encoded_state_jwt, secret, algorithms=["HS256"])
    except jwt.DecodeError as ex:
        logger.error("Decode error encountered for JWT %s", ex)
        raise VerificationException("Invalid JWT.") from ex
    except jwt.ExpiredSignatureError as ex:
        logger.error("JWT expired!")
        raise VerificationException(
            "Invalid request. Invalid state query-param."
        ) from ex
