import configparser
import logging
import os

from vja import VjaError

logger = logging.getLogger(__name__)

_DEFAULT_CONFIGDIR = os.path.expanduser("~/.vjacli")

__parser__ = None


def get_path():
    return os.path.join(get_dir(), 'vja.rc')


def get_dir():
    return os.environ.get('VJA_CONFIGDIR', _DEFAULT_CONFIGDIR)


def _load():
    filepath = get_path()
    logger.debug('Read config from %s', filepath)
    parser = configparser.ConfigParser()
    files = parser.read(filepath)
    if not files:
        raise VjaError('Could not load config file from ' + filepath)
    return parser


def get_parser():
    global __parser__
    if not __parser__:
        __parser__ = _load()
    return __parser__
