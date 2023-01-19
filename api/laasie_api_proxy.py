from flask import (
    Blueprint,
    g,
    request as flask_request,
    make_response,
)
from flask.wrappers import Response as FlaskResponse

import requests

from api import sfmc_oauth2
from api.app_logger import get_logger
from api.cookies import verify_signature
from . import env_config

API_BASE_URL = env_config.LAASIE_API_BASE_URL
bp = Blueprint("laasie_api_proxy", __name__, url_prefix="/api/laasie")
logger = get_logger(bp.name)


def bp_url_prefix() -> str:
    """
    Retruns the URL prefix in the blueprint.
    """
    if bp.url_prefix is None:
        return ""
    return bp.url_prefix


def get_request_url(request_path: str) -> str:
    """
    Returns the request URL for the customer SFMC instance.
    """
    return f"{API_BASE_URL}{request_path}"


def get_content_type(http_resp: requests.Response) -> str:
    """
    Returns the content-type header value from the response, if set,
    otherwise, returns `application/json`.
    """
    content_type = http_resp.headers.get("Content-Type")
    if content_type is None:
        return "application/json"
    else:
        return content_type


@bp.before_request
def before_request():
    """
    Middleware that executes before every request in this blueprint.
    Checks for the tenant sub-domain and the SFMC access token cookies
    and that the access token passes signature verification.
    """
    if sfmc_oauth2.ACCESS_TOKEN_COOKIE_NAME not in flask_request.cookies:
        return FlaskResponse(status=401)

    access_token = flask_request.cookies[sfmc_oauth2.ACCESS_TOKEN_COOKIE_NAME]
    decoded_token = verify_signature(access_token)

    if decoded_token is None:
        logger.error("Decoded access token value was empty. Returning a 401.")
        return FlaskResponse(status=401)

    g.decoded_token = decoded_token


@bp.route("/sfmc", methods=["POST"])
def save_sfmc_payload():
    """
    Post the server-to-server credentials to Laasie.
    """
    decoded_token = g.decoded_token

    url = get_request_url(flask_request.path.replace(bp_url_prefix(), ""))
    logger.info("proxying request to %s", url)
    http_resp = requests.post(
        url,
        json=flask_request.get_json(),
        headers={"Authorization": f"Bearer {decoded_token}"},
    )

    resp = make_response()
    resp.set_data(http_resp.content)
    resp.headers.add("Content-Type", get_content_type(http_resp))
    resp.status_code = http_resp.status_code
    return resp
