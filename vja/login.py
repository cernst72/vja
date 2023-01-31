import logging
import sys
from configparser import NoOptionError, NoSectionError

from vja import VjaError
from vja import config
from vja.apiclient import ApiClient

logger = logging.getLogger(__name__)

api_client = None


def get_client(username=None, password=None) -> ApiClient:
    global api_client
    if not api_client:
        try:
            api_client = _do_login(username, password)
        except VjaError as e:
            print(e)
            sys.exit(1)
    return api_client


def _do_login(username, password) -> ApiClient:
    try:
        api_url = config.get_parser().get('application', 'api_url')
        logger.debug('Connecting to api_url %s', api_url)
    except (NoSectionError, NoOptionError):
        raise VjaError(f'Login url not specified in {config.get_path()}.Dying.')

    client = ApiClient(api_url=api_url, username=username, password=password)
    client.authenticate()
    return client
