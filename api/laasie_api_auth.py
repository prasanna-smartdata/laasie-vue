from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Union

from flask.wrappers import Response
from flask import (
    Blueprint,
    make_response,
)

from itsdangerous import want_bytes
import requests
from werkzeug import wrappers

from api.app_logger import get_logger
from api.cookies import get_signer

from api.oauth2 import (
    InvalidTokenResponse,
)
from . import env_config

ACCESS_TOKEN_COOKIE_NAME = "external_access_token"
AUTH_BASE_URL = env_config.LAASIE_API_BASE_URL

bp = Blueprint("external_api_auth", __name__, url_prefix="/auth/laasie")
logger = get_logger(bp.name)


@dataclass
class AccessTokenResponse:
    """
    Represents an access token.
    """

    access_token: str


def from_json_dict(obj: dict[Any, Any]) -> AccessTokenResponse:
    """
    Returns an instance of the AccessTokenResponse class
    if the provided dict contains known properties. Otherwise,
    returns the dict as-is.
    """
    if obj.get("token", None) is not None:
        return AccessTokenResponse(
            access_token=obj["token"],
        )

    raise InvalidTokenResponse("dictionary is not an access token response")


def error_response():
    resp = make_response()
    resp.status_code = 500
    resp.set_data("An internal error occurred")
    return resp


@bp.route("/")
def index():
    # pylint: disable=missing-function-docstring
    logger.error("index route is not supported. Returning a 404...")
    return Response(status=404)


@bp.route("/token", methods=["POST"])
def access_token() -> Union[str, Response, wrappers.Response]:
    """
    Handles the authorization_code grant flow callback from the OAuth2 server.
    In this case, SFMC is the OAuth2 server that redirects the user's browser
    to this endpoint upon the user's successful authentication.
    """
    access_token_resp = requests.post(
        f"{AUTH_BASE_URL}/auth",
        json={
            "api_id": env_config.LAASIE_API_USERNAME,
            "api_key": env_config.LAASIE_API_PASSWORD,
        },
        headers={"Content-Type": "application/json"},
    )

    if access_token_resp.status_code != 200:
        logger.error(
            "Failed to fetch access token from Laasie (status: %d) %s",
            access_token_resp.status_code,
            str(access_token_resp.content, "UTF-8"),
        )
        return error_response()

    try:
        token = access_token_resp.json(object_hook=from_json_dict)
    except InvalidTokenResponse as ex:
        error_resp = access_token_resp.json()
        logger.error("Error parsing JSON response from token endpoint %s", ex.message)
        logger.error(error_resp)
        return error_response()

    resp = make_response()
    resp.status_code = 204

    set_cookies(resp, token)

    return resp


def set_cookies(http_resp: Response, token: AccessTokenResponse):
    """
    Sets the cookies for the external API.
    """
    signer = get_signer()
    # Access tokens are valid for 20 minutes but we'll expire the cookie
    # before then.
    # Make the access_token cookie accessible to the client.
    http_resp.set_cookie(
        ACCESS_TOKEN_COOKIE_NAME,
        str(signer.sign(want_bytes(token.access_token)), "UTF-8"),
        httponly=True,
        max_age=timedelta(minutes=60),
        samesite="None",
        secure=not env_config.IS_DEV,
    )


def delete_cookies(resp: Response):
    """
    Deletes the external API's cookies.
    """
    resp.delete_cookie(ACCESS_TOKEN_COOKIE_NAME)
