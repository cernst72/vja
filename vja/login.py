from configparser import NoOptionError, NoSectionError

from vja import VjaError
from vja import config
from vja.apiclient import ApiClient

api_client = None


def _do_login(username, password) -> ApiClient:
    """Create and initialize (including authentication) an API client."""
    try:
        api_url = config.get_parser().get("application", "api_url")
    except (NoSectionError, NoOptionError):
        raise VjaError("Login url not specified in %s.Dying." % config.get_path())

    client = ApiClient(api_url=api_url, username=username, password=password)
    client.authenticate()
    return client


def get_client(username=None, password=None) -> ApiClient:
    global api_client
    if api_client:
        return api_client
    try:
        api_client = _do_login(username, password)
        return api_client
    except VjaError as e:
        print(e)
        exit(1)
