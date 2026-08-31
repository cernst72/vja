import configparser
import logging
import os
from pathlib import Path

from vja import VjaError

logger = logging.getLogger(__name__)

_FILENAME = "config.rc"
_FILENAME_LEGACY = "vja.rc"
_TOKEN_JSON = "token.json"


class VjaConfiguration:
    def __init__(self):
        self._directory = self.find_config_path()
        self._file = self.get_config_file()
        self._parser = self._load(self._file)

    @property
    def file(self) -> Path:
        return self._file

    def get_api_url(self) -> str:
        return self._get("application", "api_url")

    def get_frontend_url(self) -> str:
        return self._get("application", "frontend_url")

    def get_token_file(self) -> Path:
        return self._directory / _TOKEN_JSON

    def get_custom_format_string(self, template_key):
        return self._parser.get("output", template_key, fallback=None)

    def get_urgency_project_keywords(self):
        return self._parser.get("urgency_keywords", "project_keywords", fallback=None)

    def get_urgency_label_keywords(self):
        return self._parser.get("urgency_keywords", "label_keywords", fallback=None)

    def get_urgency_coefficients(self) -> dict:
        try:
            return dict(self._parser.items("urgency_coefficients"))
        except (configparser.NoSectionError, configparser.NoOptionError):
            return {}

    @staticmethod
    def find_config_path() -> Path:
        # 1) $VJA_CONFIGDIR
        vja_configdir = os.getenv("VJA_CONFIGDIR")
        if vja_configdir:
            config_path = Path(vja_configdir).expanduser()
            candidate = config_path / _FILENAME
            if candidate.is_file():
                return config_path
            logger.warning(
                "VJA_CONFIGDIR is set to '%s' but '%s' was not found there.",
                config_path,
                _FILENAME,
            )

        # 2) $XDG_CONFIG_HOME/vja/config.rc
        xdg_config_home = os.getenv("XDG_CONFIG_HOME")
        if xdg_config_home:
            config_path = Path(xdg_config_home).expanduser() / "vja"
            candidate = config_path / _FILENAME
            if candidate.is_file():
                return config_path

        # 3) $HOME/.config/vja/config.rc
        config_path = Path.home() / ".config" / "vja"
        candidate = config_path / _FILENAME
        if candidate.is_file():
            return config_path

        # 4) Legacy: $HOME/.vjacli/vja.rc
        return Path.home() / ".vjacli"

    def get_config_file(self) -> Path:
        if self._directory.name != ".vjacli":
            return self._directory / _FILENAME
        logger.info(
            "Using legacy config path %s. Please move your config file (and token.json) to %s.",
            self._directory / _FILENAME_LEGACY,
            self._directory.parent / ".config" / "vja" / _FILENAME,
        )
        return self._directory / _FILENAME_LEGACY

    @staticmethod
    def _load(filepath: Path):
        logger.debug("Read config from %s", filepath.resolve())
        parser = configparser.RawConfigParser()
        if not parser.read(filepath):
            msg = f"Could not load config file from {filepath.resolve()}"
            raise VjaError(msg)
        return parser

    def _get(self, section, option) -> str:
        try:
            return self._parser.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError) as ex:
            msg = f"[{section}] [{option}] not specified in {self.file}. Dying."
            raise VjaError(msg) from ex
