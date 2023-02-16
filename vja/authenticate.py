import json
import logging
import os

import click
import requests

from vja import VjaError

logger = logging.getLogger(__name__)


class Login:
    def __init__(self, api_url, token_file):
        self._api_url = api_url
        self._token_file = token_file
        self._token = {'access': None}

    @property
    def _access_token(self):
        if not self._token['access']:
            raise KeyError('access token not set! call authenticate()')
        return self._token['access']

    def _load_access_token(self):
        try:
            with open(self._token_file, encoding='utf-8') as token_file:
                data = json.load(token_file)
        except IOError:
            return False
        self._token['access'] = data['token']
        if not self._token['access']:
            return False
        return True

    def _store_access_token(self):
        data = {'token': self._access_token}
        with open(self._token_file, 'w', encoding="utf-8") as token_file:
            json.dump(data, token_file)

    def _create_url(self, path):
        return self._api_url + path

    @staticmethod
    def _to_json(response: requests.Response):
        try:
            return response.json()
        except Exception as e:
            logger.error('Expected valid json, but found %s', response.text)
            raise VjaError('Cannot parse json in response.') from e

    def validate_access_token(self, force=False, username=None, password=None, totp_passcode=None):
        if self._load_access_token() and not force:
            return
        login_url = self._create_url('/login')
        click.echo(f'Login to {login_url}')
        username = username or click.prompt('Username')
        password = password or click.prompt('Password', hide_input=True)
        payload = {'username': username,
                   'password': password,
                   'totp_passcode': totp_passcode}
        response = requests.post(login_url, json=payload, timeout=30)
        response.raise_for_status()
        self._token['access'] = self._to_json(response)['token']
        self._store_access_token()
        logger.info('Login successful.')

    def get_auth_header(self):
        return {'Authorization': f'Bearer {self._access_token}'}

    def logout(self):
        if os.path.isfile(self._token_file):
            os.remove(self._token_file)
