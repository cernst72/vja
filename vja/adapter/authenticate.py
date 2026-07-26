import json
import logging
import os
import time

import click
import jwt
import requests
from requests import Response

from vja import VjaError
from vja.adapter.http_util import response_to_json

logger = logging.getLogger(__name__)


class Login:
    def __init__(self, api_url, token_file):
        self._api_url = api_url
        self._token_file = token_file
        self._token: dict[str, str | None] = {"access": None, "refresh": None}

    @property
    def _access_token(self):
        if not self._token["access"]:
            msg = "access token not set! call authenticate()"
            raise VjaError(msg)
        return self._token["access"]

    @property
    def _refresh_token(self):
        return self._token["refresh"] or None

    def validate_access_token(
        self, force=False, username=None, password=None, totp_passcode=None
    ):
        if self._load_tokens_from_file() and not force:
            try:
                self._refresh_proactively()
            except Exception:
                # ignore, use expired token to trigger 401 and refresh in authenticate()
                pass
            return
        self._prompt_and_login(username, password, totp_passcode)

    def _prompt_and_login(self, username=None, password=None, totp_passcode=None):
        username = username or click.prompt("Username")
        password = password or click.prompt("Password", hide_input=True)
        response = self._post_login_request(username, password, totp_passcode)
        if response.status_code == 412:
            payload = response_to_json(response)
            if payload.get("detail") == "Invalid totp passcode.":
                totp_passcode = totp_passcode or click.prompt("One-time password")
                response = self._post_login_request(username, password, totp_passcode)
        if (
            response.status_code == 412
            and response_to_json(response)["message"] == "Invalid totp passcode."
        ):
            totp_passcode = totp_passcode or click.prompt("One-time password")
            response = self._post_login_request(username, password, totp_passcode)
        response.raise_for_status()
        self._update_tokens(response)
        logger.info("Login successful.")

    def refresh_access_token(self):
        refresh_token = self._refresh_token
        if not refresh_token:
            msg = "refresh token not set! call authenticate()"
            raise VjaError(msg)
        logger.debug("Refreshing access token")
        refresh_url = f"{self._api_url}/user/token/refresh"
        cookies = {"vikunja_refresh_token": refresh_token}
        response = requests.post(refresh_url, cookies=cookies, timeout=30)
        response.raise_for_status()
        self._update_tokens(response)

    def get_auth_header(self):
        return {"Authorization": f"Bearer {self._access_token}"}

    def logout(self):
        if self._load_tokens_from_file():
            response = requests.post(
                f"{self._api_url}/user/logout",
                headers=self.get_auth_header(),
                timeout=10,
            )
            logger.debug("logout: %s", response.text)
        if os.path.isfile(self._token_file):
            os.remove(self._token_file)
        self._token = {"access": None, "refresh": None}

    def _load_tokens_from_file(self):
        try:
            with open(self._token_file, encoding="utf-8") as token_file:
                data = json.load(token_file)
        except OSError:
            return False
        self._token["access"] = data.get("token")
        if not self._token["access"]:
            return False
        self._token["refresh"] = data.get("refresh")
        return True

    def _store_tokens_to_file(self):
        data = {"token": self._access_token}
        if self._refresh_token:
            data["refresh"] = self._refresh_token
        with open(self._token_file, "w", encoding="utf-8") as token_file:
            json.dump(data, token_file)

    def _refresh_proactively(self):
        # refresh if token will be expired within 60 seconds
        access_token = self._token.get("access")
        if not access_token:
            return
        exp = self._jwt_expiry(access_token)
        if exp and exp < time.time() + 60:
            logger.debug("refresh access token proactively")
            self.refresh_access_token()

    def _update_tokens(self, response: Response):
        self._token["access"] = response_to_json(response)["token"]
        new_refresh_token = response.cookies.get("vikunja_refresh_token")
        if new_refresh_token:
            self._token["refresh"] = new_refresh_token
        self._store_tokens_to_file()

    def _post_login_request(self, username, password, totp_passcode):
        login_url = f"{self._api_url}/login"
        payload = {
            "long_token": True,
            "username": username,
            "password": password,
            "totp_passcode": totp_passcode,
        }
        return requests.post(login_url, json=payload, timeout=30)

    @staticmethod
    def _jwt_expiry(token: str):
        exp = jwt.decode(token, options={"verify_signature": False}).get("exp")
        return int(exp) if exp else None
