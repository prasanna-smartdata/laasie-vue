"""
The API backend for the Laasie SFMC application.
"""
import os

from flask_wtf.csrf import CSRFProtect, CSRFError, generate_csrf  # type: ignore

from flask.wrappers import Response
from flask import (
    Flask,
    flash,
    make_response,
    redirect,
    render_template,
    g,
    request as flask_request,
)

from api.app_logger import get_logger
from . import env_config

from . import sfmc_oauth2
from . import laasie_api_auth
from . import sfmc_api_proxy
from . import laasie_api_proxy

logger = get_logger("app-main")
csrf = CSRFProtect()

# The request path where the custom content block is served.
CONTENTBLOCK_REQUEST_PATH = "/contentblock"

# create_app is used as the app factory in the Dockerfile.
# Be sure to update the Dockerfile if you are changing the
# name of this function.
def create_app(test_config=None):
    """
    Create an instance of the Flask application.
    """
    app = Flask(__name__, static_folder="ui", static_url_path="/ui")

    csrf.init_app(app)

    # Load the instance config, if it exists, when not testing.
    if test_config is None:
        logger.info("Loading environment config")
        app.config.from_object(env_config)
    else:
        logger.info("Loading provided test config: %s", test_config)
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError as ex:
        if not isinstance(ex, FileExistsError):
            logger.error(
                "Could not create instance folder: %s %s", ex.strerror, ex.errno
            )

    app.register_blueprint(sfmc_oauth2.bp)
    app.register_blueprint(laasie_api_auth.bp)
    app.register_blueprint(sfmc_api_proxy.bp)
    app.register_blueprint(laasie_api_proxy.bp)

    @app.route("/healthcheck")
    def heartbeat():
        return Response(status=200, response="Healthy!")

    @app.route("/logout", methods=["POST"])
    def logout():
        resp = make_response()
        resp.status_code = 204
        sfmc_oauth2.delete_cookies(resp)
        laasie_api_auth.delete_cookies(resp)
        return resp

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):
        # pylint: disable=unused-argument
        logger.debug("catch_all request path %s", flask_request.path)
        if flask_request.path in [
            "/favicon.ico",
            f"{CONTENTBLOCK_REQUEST_PATH}/dragIcon.png",
            f"{CONTENTBLOCK_REQUEST_PATH}/favicon.ico",
            f"{CONTENTBLOCK_REQUEST_PATH}/icon.png",
        ]:
            return app.send_static_file(
                flask_request.path.removeprefix(f"{CONTENTBLOCK_REQUEST_PATH}/")
            )

        generate_csrf()

        if env_config.REDIRECT_UI_TO_LOCALHOST:
            url = f"https://app.localhost:3000/ui{flask_request.path}"
            logger.info("Redirecting to: %s", url)
            return redirect(url)

        return app.send_static_file("index.html")

    @app.errorhandler(404)
    def page_not_found(error):
        # pylint: disable=unused-argument
        return app.send_static_file("index.html")

    @app.errorhandler(CSRFError)
    def handle_csrf_error(error):
        flash(error.description, "error")
        return render_template("oauth2/error.html"), 400

    @app.after_request
    def after_request(resp: Response):
        # The following settings are mostly an implementation of
        # the recommendations from Flask's security guide.
        # https://flask.palletsprojects.com/en/2.1.x/security/

        # Disallow anyone besides SFMC from embedding our app.
        resp.content_security_policy.frame_ancestors = (
            "https://*.exacttarget.com https://*.marketingcloudapps.com"
        )
        # The following CSP allows scripts and API requests to be loaded
        # from this (self) server. Additionally, we allow our app to
        # make API requests to known API hosts.
        resp.content_security_policy.default_src = "'self'"
        resp.content_security_policy.img_src = "'self' data:"
        resp.content_security_policy.script_src = "'self'"
        resp.content_security_policy.connect_src = (
            "'self' https://*.marketingcloudapis.com/"
        )
        resp.content_security_policy.object_src = "'none'"
        resp.headers.add("X-Content-Type-Options", "nosniff")

        if "csrf_token" in g:
            resp.set_cookie(
                "X-CSRF-Token",
                g.csrf_token,
                httponly=False,
                samesite="None",
                secure=not env_config.IS_DEV,
            )

        return resp

    return app
