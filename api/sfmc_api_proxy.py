from flask import (
    Blueprint,
    g,
    jsonify,
    request as flask_request,
    make_response,
)
from flask.wrappers import Response as FlaskResponse
import requests
from api import sfmc_oauth2

from api.app_logger import get_logger
from api.cookies import verify_signature


bp = Blueprint("sfmc_api_proxy", __name__, url_prefix="/api/sfmc")
logger = get_logger(bp.name)


def bp_url_prefix() -> str:
    """
    Retruns the URL prefix in the blueprint.
    """
    if bp.url_prefix is None:
        return ""
    return bp.url_prefix


def get_request_url(tenant_subdomain: str, request_path: str) -> str:
    """
    Returns the request URL for the customer SFMC instance.
    """
    return f"https://{tenant_subdomain}.rest.marketingcloudapis.com{request_path}"


def get_content_type(http_resp: requests.Response) -> str:
    """
    Returns the content-type header value from the response, if set,
    otherwise, returns `application/json`.
    """
    sfmc_content_type = http_resp.headers.get("Content-Type")
    if sfmc_content_type is None:
        return "application/json"
    else:
        return sfmc_content_type


@bp.before_request
def before_request():
    """
    Middleware that executes before every request in this blueprint.
    Checks for the tenant sub-domain and the SFMC access token cookies
    and that the access token passes signature verification.
    """
    if sfmc_oauth2.TSSD_COOKIE_NAME not in flask_request.cookies:
        logger.error("tssd cookie was empty.")
        return FlaskResponse(status=401)

    tssd = flask_request.cookies[sfmc_oauth2.TSSD_COOKIE_NAME]
    if sfmc_oauth2.tssd_regex.fullmatch(tssd) is None:
        logger.error("Invalid value provided in the tssd param.")
        return jsonify(
            error="invalid_request",
            error_description="Invalid value provided for the tssd param.",
        )

    if sfmc_oauth2.ACCESS_TOKEN_COOKIE_NAME not in flask_request.cookies:
        return FlaskResponse(status=401)

    tenant_subdomain = tssd
    access_token = flask_request.cookies[sfmc_oauth2.ACCESS_TOKEN_COOKIE_NAME]
    decoded_token = verify_signature(access_token)

    if decoded_token is None:
        logger.error("Decoded access token value was empty. Returning a 401.")
        return FlaskResponse(status=401)

    g.tenant_subdomain = tenant_subdomain
    g.decoded_token = decoded_token


@bp.route("/asset/v1/content/assets")
def filter_assets():
    """
    Lists assets by using a simple filter.
    """
    tenant_subdomain = g.tenant_subdomain
    decoded_token = g.decoded_token

    url = get_request_url(
        tenant_subdomain, flask_request.path.replace(bp_url_prefix(), "")
    )
    logger.info("proxying request to %s", url)
    http_resp = requests.get(
        url,
        flask_request.args.to_dict(),
        headers={"Authorization": f"Bearer {decoded_token}"},
    )

    resp = make_response()
    resp.set_data(http_resp.content)
    resp.headers.add("Content-Type", get_content_type(http_resp))
    resp.status_code = http_resp.status_code
    return resp


@bp.route("/userinfo")
def get_user_info():
    """
    Get the currently logged-in user's info.
    """
    tenant_subdomain = g.tenant_subdomain
    decoded_token = g.decoded_token

    # https://developer.salesforce.com/docs/marketing/marketing-cloud/guide/getUserInfo.html
    url = f"https://{tenant_subdomain}.auth.marketingcloudapis.com/v2/userinfo"
    logger.info("proxying request to %s", url)
    http_resp = requests.get(
        url,
        flask_request.args.to_dict(),
        headers={"Authorization": f"Bearer {decoded_token}"},
    )

    resp = make_response()
    resp.set_data(http_resp.content)
    resp.headers.add("Content-Type", get_content_type(http_resp))
    resp.status_code = http_resp.status_code
    return resp


@bp.route("/asset/v1/content/assets/query", methods=["POST"])
def advanced_filter_assets():
    """
    Lists assets by using an advanced filter. The filter query
    must be passed in the request body.
    """
    tenant_subdomain = g.tenant_subdomain
    decoded_token = g.decoded_token

    url = get_request_url(
        tenant_subdomain, flask_request.path.replace(bp_url_prefix(), "")
    )
    logger.info("proxying request to %s", url)
    http_resp = requests.post(
        url,
        data=flask_request.data,
        headers={
            "Authorization": f"Bearer {decoded_token}",
            "Content-Type": "application/json",
        },
    )

    resp = make_response()
    resp.set_data(http_resp.content)
    resp.headers.add("Content-Type", get_content_type(http_resp))
    resp.status_code = http_resp.status_code
    return resp


@bp.route("/asset/v1/content/assets", methods=["POST"])
def create_asset():
    """
    Create an asset.
    """
    tenant_subdomain = g.tenant_subdomain
    decoded_token = g.decoded_token

    url = get_request_url(
        tenant_subdomain, flask_request.path.replace(bp_url_prefix(), "")
    )
    logger.info("proxying request to %s", url)
    http_resp = requests.post(
        url,
        data=flask_request.data,
        headers={"Authorization": f"Bearer {decoded_token}"},
    )

    resp = make_response()
    resp.set_data(http_resp.content)
    resp.headers.add("Content-Type", get_content_type(http_resp))
    resp.status_code = http_resp.status_code
    return resp


@bp.route("/asset/v1/content/assets/<asset_id>", methods=["PATCH"])
def update_asset(asset_id: int):
    """
    Update an existing asset.
    """
    # pylint: disable=unused-argument
    tenant_subdomain = g.tenant_subdomain
    decoded_token = g.decoded_token

    url = get_request_url(
        tenant_subdomain, flask_request.path.replace(bp_url_prefix(), "")
    )
    logger.info("proxying request to %s", url)
    http_resp = requests.patch(
        url,
        data=flask_request.data,
        headers={
            "Authorization": f"Bearer {decoded_token}",
            "Content-Type": "application/json",
        },
    )

    resp = make_response()
    resp.set_data(http_resp.content)
    resp.headers.add("Content-Type", get_content_type(http_resp))
    resp.status_code = http_resp.status_code
    return resp


@bp.route("/asset/v1/assets/<asset_id>/thumbnail")
def get_thumbnail_base64(asset_id: int):
    """
    Get the base64-encoded string of an asset's thumbnail.
    """
    # pylint: disable=unused-argument
    tenant_subdomain = g.tenant_subdomain
    decoded_token = g.decoded_token

    url = get_request_url(
        tenant_subdomain, flask_request.path.replace(bp_url_prefix(), "")
    )
    logger.info("proxying request to %s", url)
    http_resp = requests.get(
        url,
        data=flask_request.data,
        headers={"Authorization": f"Bearer {decoded_token}"},
    )

    resp = make_response()
    resp.set_data(http_resp.content)
    resp.headers.add("Content-Type", get_content_type(http_resp))
    resp.status_code = http_resp.status_code
    return resp


@bp.route("/asset/v1/content/categories")
def list_categories():
    """
    Lists categories.
    """
    tenant_subdomain = g.tenant_subdomain
    decoded_token = g.decoded_token

    url = get_request_url(
        tenant_subdomain, flask_request.path.replace(bp_url_prefix(), "")
    )
    logger.info("proxying request to %s", url)
    http_resp = requests.get(
        url,
        flask_request.args.to_dict(),
        headers={"Authorization": f"Bearer {decoded_token}"},
    )

    resp = make_response()
    resp.set_data(http_resp.content)
    resp.headers.add("Content-Type", get_content_type(http_resp))
    resp.status_code = http_resp.status_code
    return resp


@bp.route("/asset/v1/content/categories", methods=["POST"])
def create_category():
    """
    Create a category in Content Builder.
    """
    tenant_subdomain = g.tenant_subdomain
    decoded_token = g.decoded_token

    url = get_request_url(
        tenant_subdomain, flask_request.path.replace(bp_url_prefix(), "")
    )
    logger.info("proxying request to %s", url)
    http_resp = requests.post(
        url,
        data=flask_request.data,
        headers={"Authorization": f"Bearer {decoded_token}"},
    )

    resp = make_response()
    resp.set_data(http_resp.content)
    resp.headers.add("Content-Type", get_content_type(http_resp))
    resp.status_code = http_resp.status_code
    return resp
