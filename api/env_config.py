import os
from typing import Optional
from dotenv import load_dotenv


def _assert_not_none_or_empty(str_value: Optional[str]):
    if str_value is None or str_value.strip() == "":
        raise RuntimeError("value is required!")


FLASK_DEBUG = os.getenv("FLASK_DEBUG")
print(f"FLASK_DEBUG:{FLASK_DEBUG}")

IS_DEV = FLASK_DEBUG == "True"

FLASK_TESTING = os.getenv("FLASK_TESTING")

if FLASK_TESTING == "True":
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env.test"))
else:
    load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
_assert_not_none_or_empty(JWT_SECRET)

SELF_DOMAIN = os.getenv("SELF_DOMAIN", "localhost")

SECRET_KEY = os.getenv("SECRET_KEY")
_assert_not_none_or_empty(SECRET_KEY)

# Any session cookies set via Flask should set the
# SameSite attribute to `'None'`
# (string value; not the None type in Python.)
SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = FLASK_DEBUG != "development"
SESSION_USE_SIGNER = True

SFMC_OAUTH2_CALLBACK_PATH = os.getenv("SFMC_OAUTH2_CALLBACK_PATH", "/callback")

SFMC_CLIENT_ID = os.getenv("SFMC_CLIENT_ID")
_assert_not_none_or_empty(SFMC_CLIENT_ID)

SFMC_CLIENT_SECRET = os.getenv("SFMC_CLIENT_SECRET")
_assert_not_none_or_empty(SFMC_CLIENT_SECRET)

SFMC_DEFAULT_TENANT_SUBDOMAIN = os.getenv("SFMC_DEFAULT_TENANT_SUBDOMAIN", "")

LAASIE_API_BASE_URL = os.getenv("LAASIE_API_BASE_URL", "")
LAASIE_API_USERNAME = os.getenv("LAASIE_API_USERNAME", "")
LAASIE_API_PASSWORD = os.getenv("LAASIE_API_PASSWORD", "")

redirectUiToLocalhost = os.getenv("REDIRECT_UI_TO_LOCALHOST", "")
REDIRECT_UI_TO_LOCALHOST = True
if redirectUiToLocalhost == "" or redirectUiToLocalhost == "False":
    REDIRECT_UI_TO_LOCALHOST = False
