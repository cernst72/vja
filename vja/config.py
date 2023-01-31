import configparser
import logging
import os

from vja import VjaError

logger = logging.getLogger(__name__)

_DEFAULT_CONFIGDIR = os.path.expanduser("~/.vjacli")


def get_path():
    """Return default config file path."""
    return os.path.join(get_dir(), "vja.rc")


def get_dir():
    """Return default config file path."""
    return os.environ.get('VJA_CONFIGDIR', _DEFAULT_CONFIGDIR)


def load():
    """Load config file."""
    filepath = get_path()
    logger.debug("Read config from %s " % filepath)
    parser = configparser.SafeConfigParser()
    parser.read(filepath)
    return parser


def store(config):
    """Store the config to the file."""
    if not os.path.exists(get_dir()):
        os.mkdir(get_dir())
    with open(get_path(), "w") as cfile:
        config.write(cfile)


def reload(parser):
    """Reload the config file."""
    filepath = get_path()
    parser.read(filepath)


__parser__ = load()


def get_parser():
    """Get the config parser."""
    if not __parser__:
        raise VjaError("config file is not loaded.")
    else:
        return __parser__
