import logging

import requests

from vja import VjaError

logger = logging.getLogger(__name__)


def response_to_json(response: requests.Response):
    try:
        return response.json()
    except Exception as e:
        logger.exception("Expected valid json, but found %s", response.text)
        msg = "Cannot parse json in response."
        raise VjaError(msg) from e
