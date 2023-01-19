import flask
from itsdangerous import want_bytes

from api import create_app
from api.cookies import get_signer, verify_signature
from api.sfmc_oauth2 import tssd_regex


def test_tssd_re_success():
    assert tssd_regex.fullmatch("mcmb4wk3d-v6tlqyshbytqf09gsq") is not None
    assert tssd_regex.fullmatch("mcmb4wk3d") is not None


def test_verification():
    flask.current_app = create_app()
    expected_token = "fake_token"
    with flask.current_app.app_context():
        signer = get_signer()
        signed_token = signer.sign(want_bytes(expected_token))
        decoded_token = verify_signature(str(signed_token, "UTF-8"))
        assert decoded_token == expected_token
