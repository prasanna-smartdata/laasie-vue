from typing import Optional
from flask import current_app
from itsdangerous import BadSignature, Signer
from api.app_logger import get_logger

logger = get_logger("cookies")


def get_signer():
    """
    Returns a Signer.
    """
    return Signer(current_app.secret_key, salt="flask-session", key_derivation="hmac")


def verify_signature(value: str) -> Optional[str]:
    """
    Validates the signature of the provided value and returns
    the decoded value if the signature is valid. Otherwise,
    returns None.
    """
    signer = get_signer()
    try:
        value_as_bytes = signer.unsign(value)
        return value_as_bytes.decode()
    except UnicodeDecodeError as ex:
        logger.error("Invalid cookie signature %s", ex.reason)
    except BadSignature as ex:
        logger.error("Failed signature verification %s", ex.message)

    return None
