import configparser
import logging
import os

from vja import VjaError

logger = logging.getLogger(__name__)

_DEFAULT_CONFIGDIR = os.path.expanduser("~/.vjacli")
_FILENAME = 'vja.rc'
_TOKEN_JSON = 'token.json'


class VjaConfiguration:

    def __init__(self):
        self._directory = os.environ.get('VJA_CONFIGDIR', _DEFAULT_CONFIGDIR)
        self._file = os.path.join(self._directory, _FILENAME)
        self._parser = self._load(self._file)

    @staticmethod
    def _load(filepath):
        logger.debug('Read config from %s', filepath)
        parser = configparser.ConfigParser()
        if not parser.read(filepath):
            raise VjaError('Could not load config file from ' + filepath)
        return parser

    @property
    def file(self):
        return self._file

    def get_api_url(self):
        return self._get('application', 'api_url')

    def get_frontend_url(self):
        return self._get('application', 'frontend_url')

    def get_token_file(self):
        return os.path.join(self._directory, _TOKEN_JSON)

    def _get(self, section, option):
        try:
            return self._parser.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError) as ex:
            raise VjaError(f'[{section}] [{option}] not specified in {self.file}. Dying.') from ex
