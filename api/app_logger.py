import logging

from flask import has_request_context, request

from . import env_config


class RequestFormatter(logging.Formatter):
    """
    Implements the logging.Formatter
    """

    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


formatter = RequestFormatter(
    "%(remote_addr)s [%(asctime)s] ::%(name)s:: %(levelname)s: %(message)s"
)


def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger instance for the given name.
    """
    logger = logging.getLogger(name)
    if env_config.FLASK_DEBUG != "1":
        gunicorn_logger = logging.getLogger("gunicorn.error")
        logger.handlers.extend(gunicorn_logger.handlers)
        for h in logger.handlers:
            h.setFormatter(formatter)
    else:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    if env_config.FLASK_DEBUG == "1":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    return logger
