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
        with open(self._token_file, 'w', encoding='utf-8') as token_file:
            json.dump(data, token_file)

    def _create_url(self, path):
        return self._api_url + path

    def validate_access_token(self, force=False, username=None, password=None, totp_passcode=None):
        if self._load_access_token() and not force:
            return
        username = username or click.prompt('Username')
        password = password or click.prompt('Password', hide_input=True)
        response = self._post_login_request(username, password, totp_passcode)
        if response.status_code == 412 and self._to_json(response)['message'] == 'Invalid totp passcode.':
            totp_passcode = totp_passcode or click.prompt('One-time password')
            response = self._post_login_request(username, password, totp_passcode)
        response.raise_for_status()
        self._token['access'] = self._to_json(response)['token']
        self._store_access_token()
        logger.info('Login successful.')

    def get_auth_header(self):
        return {'Authorization': f'Bearer {self._access_token}'}

    def logout(self):
        if os.path.isfile(self._token_file):
            os.remove(self._token_file)

    def _post_login_request(self, username, password, totp_passcode):
        login_url = self._create_url('/login')
        payload = {'username': username,
                   'password': password,
                   'totp_passcode': totp_passcode}
        return requests.post(login_url, json=payload, timeout=30)

    @staticmethod
    def _to_json(response: requests.Response):
        try:
            return response.json()
        except Exception as e:
            logger.error('Expected valid json, but found %s', response.text)
            raise VjaError('Cannot parse json in response.') from e
