from dataclasses import dataclass
from datetime import timedelta
import re
from typing import Any, Union

from flask.wrappers import Response
from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request as flask_request,
    make_response,
    url_for,
)
from itsdangerous import want_bytes
import requests
from werkzeug import wrappers

from api.app_logger import get_logger
from api.cookies import get_signer, verify_signature

from api.oauth2 import (
    AuthorizationParamsException,
    InvalidRequestException,
    InvalidTokenResponse,
    get_encoded_state_jwt,
    pre_oauth2_callback,
)
from . import env_config

ACCESS_TOKEN_COOKIE_NAME = "sfmc_access_token"
REFRESH_TOKEN_COOKIE_NAME = "sfmc_refresh_token"
TSSD_COOKIE_NAME = "sfmc_tssd"

bp = Blueprint("sfmc_oauth2", __name__, url_prefix="/oauth2/sfmc")
logger = get_logger(bp.name)
# tssd is the tenant sub-domain. In other words, the customer's SFMC
# sub-domain.
# https://developer.salesforce.com/docs/marketing/marketing-cloud/guide/authorization-code.html#authorization-code-return
tssd_regex = re.compile("[a-zA-Z0-9-]+")
default_tenant_subdomain = env_config.SFMC_DEFAULT_TENANT_SUBDOMAIN


@dataclass
class AccessTokenResponse:
    """
    Represents an access token returned from SFMC.
    """

    access_token: str
    expires_in: int
    refresh_token: str
    rest_instance_url: str
    scope: str
    soap_instance_url: str


def from_json_dict(obj: dict[Any, Any]) -> Union[AccessTokenResponse, dict]:
    """
    Returns an instance of the AccessTokenResponse class
    if the provided dict contains known properties. Otherwise,
    returns the dict as-is.
    """
    if obj.get("access_token", None) is not None:
        return AccessTokenResponse(
            access_token=obj["access_token"],
            expires_in=obj["expires_in"],
            refresh_token=obj["refresh_token"],
            rest_instance_url=obj["rest_instance_url"],
            scope=obj["scope"],
            soap_instance_url=obj["soap_instance_url"],
        )

    raise InvalidTokenResponse("dictionary is not an access token response")


@bp.route("/")
def index():
    # pylint: disable=missing-function-docstring
    logger.error("index route is not supported. Returning a 404...")
    return Response(status=404)


@bp.route("/authorize")
def authorize():
    """
    Redirects the user to the SFMC user authorization endpoint.
    """
    if env_config.JWT_SECRET is None:
        logger.error("JWT_SECRET is required")
        raise AuthorizationParamsException("Cannot build authorization URL")

    url = f"https://{default_tenant_subdomain}.auth.marketingcloudapis.com/v2/authorize?client_id={env_config.SFMC_CLIENT_ID}&response_type=code&redirect_uri={env_config.SELF_DOMAIN}{bp.url_prefix}/callback"
    encoded_state_jwt = get_encoded_state_jwt(env_config.JWT_SECRET)
    return redirect(f"{url}&state={encoded_state_jwt}")


@bp.route(env_config.SFMC_OAUTH2_CALLBACK_PATH)
def oauth2_callback() -> Union[str, Response, wrappers.Response]:
    """
    Handles the authorization_code grant flow callback from the OAuth2 server.
    In this case, SFMC is the OAuth2 server that redirects the user's browser
    to this endpoint upon the user's successful authentication.
    """
    try:
        pre_oauth2_callback()
    except InvalidRequestException as ex:
        flash(ex.message, "error")
        return render_template("oauth2/error.html")

    code = flask_request.args.get("code")
    tenant_subdomain = default_tenant_subdomain
    # tssd is the end-user's subdomain. If present, we should use that.
    tssd = flask_request.args.get("tssd")

    if tssd is not None:  # Validate the format of the tssd param.
        if tssd_regex.fullmatch(tssd) is None:
            flash("Invalid value provided in the tssd param.", "error")
            return render_template("oauth2/error.html")
        tenant_subdomain = tssd

    access_token_resp = requests.post(
        f"https://{tenant_subdomain}.auth.marketingcloudapis.com/v2/token",
        json={
            "client_id": env_config.SFMC_CLIENT_ID,
            "client_secret": env_config.SFMC_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": f"{env_config.SELF_DOMAIN}{bp.url_prefix}/callback",
        },
    )

    if access_token_resp.status_code != 200:
        error_resp = access_token_resp.json()
        logger.error(
            "Failed to fetch access token from SFMC. %s",
            error_resp["error_description"],
        )
        flash(error_resp["error_description"], "error")
        return render_template("oauth2/error.html")

    token: AccessTokenResponse
    try:
        token = access_token_resp.json(object_hook=from_json_dict)
    except InvalidTokenResponse as ex:
        logger.error("Parsing JSON response from token endpoint %s", ex.message)
        flash(ex.message, "error")
        return render_template("oauth2/error.html")

    resp = make_response(redirect(url_for("catch_all")))

    set_cookies(resp, token, tenant_subdomain)

    return resp


@bp.route("/refresh_token", methods=["POST"])
def refresh_token():
    """
    Called by the UI periodically to refresh its access token
    and the refresh token.
    """
    if TSSD_COOKIE_NAME not in flask_request.cookies:
        return Response(status=401)
    if REFRESH_TOKEN_COOKIE_NAME not in flask_request.cookies:
        return Response(status=401)

    tssd = flask_request.cookies[TSSD_COOKIE_NAME]
    refresh_token_cookie_value = flask_request.cookies[REFRESH_TOKEN_COOKIE_NAME]

    if refresh_token_cookie_value is None:
        logger.error(
            "%s cookie was not found. Returning 401.", REFRESH_TOKEN_COOKIE_NAME
        )
        return Response(status=401)
    if tssd is None:
        logger.error("SFMC tenant sub-domain cookie was not found.")
        return Response(status=401)

    if tssd_regex.fullmatch(tssd) is None:
        logger.error("Invalid value provided in the tssd param.")
        return jsonify(
            error="invalid_request",
            error_description="Invalid value provided for the tssd param.",
        )
    tenant_subdomain = tssd

    decoded_rt = verify_signature(refresh_token_cookie_value)
    if decoded_rt is None:
        logger.error("Decoded refresh token value was empty. Returning a 401.")
        return Response(status=401)

    access_token_resp = requests.post(
        f"https://{tenant_subdomain}.auth.marketingcloudapis.com/v2/token",
        json={
            "grant_type": "refresh_token",
            "client_id": env_config.SFMC_CLIENT_ID,
            "client_secret": env_config.SFMC_CLIENT_SECRET,
            "refresh_token": decoded_rt,
        },
    )

    if access_token_resp.status_code != 200:
        error_resp = access_token_resp.json()
        logger.error("Failed to fetch refresh token from SFMC: %s", error_resp)
        if error_resp["error"] == "invalid_request":
            return Response(status=401)
        if error_resp["error"] == "invalid_token":
            return Response(status=400)
        return Response(status=500)

    try:
        token = access_token_resp.json(object_hook=from_json_dict)
    except InvalidTokenResponse as ex:
        logger.error(
            "Failed to refresh token. Error parsing JSON response from token endpoint: %s",
            ex.message,
        )
        return Response(status=500)

    http_resp = make_response()

    set_cookies(http_resp, token, tenant_subdomain)

    return http_resp


def set_cookies(http_resp: Response, token: AccessTokenResponse, tenant_subdomain: str):
    """
    Sets the SFMC cookies.
    """
    # Set the tenant subdomain cookie again to refresh its max_age.
    http_resp.set_cookie(
        TSSD_COOKIE_NAME,
        tenant_subdomain,
        httponly=True,
        max_age=timedelta(days=1),
        samesite="None",
        secure=not env_config.IS_DEV,
    )

    signer = get_signer()
    # Access tokens are valid for 20 minutes but we'll expire the cookie
    # before then.
    http_resp.set_cookie(
        ACCESS_TOKEN_COOKIE_NAME,
        str(signer.sign(want_bytes(token.access_token)), "UTF-8"),
        httponly=True,
        max_age=timedelta(minutes=20),
        samesite="None",
        secure=not env_config.IS_DEV,
    )
    # But not the refresh_token cookie since we only want the server to be
    # able to access it and we only want it for the duration of the session.
    http_resp.set_cookie(
        REFRESH_TOKEN_COOKIE_NAME,
        str(signer.sign(want_bytes(token.refresh_token)), "UTF-8"),
        httponly=True,
        samesite="None",
        secure=not env_config.IS_DEV,
        max_age=timedelta(days=14),
    )


def delete_cookies(resp: Response):
    """
    Deletes the SFMC cookies.
    """
    resp.delete_cookie(ACCESS_TOKEN_COOKIE_NAME)
    resp.delete_cookie(REFRESH_TOKEN_COOKIE_NAME)
    resp.delete_cookie(TSSD_COOKIE_NAME)
