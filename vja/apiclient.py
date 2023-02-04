import json
import logging
import os
import sys
from functools import wraps

import click
import requests

from vja import VjaError

logger = logging.getLogger(__name__)


def check_access_token(func):
    """ A decorator that makes the decorated function check for access token."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Provide decorated function with `access_token` provided as a keword
        argument.
        """
        # check if `access_token` is set to a value in kwargs
        if 'access_token' in kwargs and kwargs['access_token'] is not None:
            return func(*args, **kwargs)
        # try to get the access token
        try:
            self = args[0]
            self.get_access_token()
            return func(*args, **kwargs)
        except KeyError as e:
            raise VjaError(f'need access token to call function {func.__name__}; call authenticate()') from e

    return wrapper


def handle_http_error(func):
    """A decorator to handle some HTTP errors raised in decorated function f."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Handle the HTTPError exceptions raised in f."""
        try:
            return func(*args, **kwargs)
        except requests.HTTPError as error:
            if error.response.status_code in (401, 429):
                logger.info('HTTP-Error %s, url=%s; trying to retrieve new access token...',
                            error.response.status_code, error.response.url)
                self = args[0]
                self.get_access_token(force=True)
                return func(*args, **kwargs)  # try again with new token. Re-raise if failed.

            logger.warning('HTTP-Error %s, url=%s, body=%s',
                           error.response.status_code, error.response.url, error.response.text)
            sys.exit(1)

    return wrapper


class ApiClient:
    def __init__(self, api_url, token_file):
        logger.debug('Connecting to api_url %s', api_url)
        self._api_url = api_url
        self._token_file = token_file
        self._token = {'access': None}
        self._cache = {'lists': None, 'labels': None, 'namespaces': None, 'tasks': None}

    @property
    def access_token(self):
        """Property for accessing the cached access token."""
        if not self._token['access']:
            raise KeyError('access token not set! call authenticate()')
        return self._token['access']

    def create_url(self, path):
        return self._api_url + path

    def authenticate(self, username=None, password=None):
        self.get_access_token(True, username, password)

    def load_access_token(self):
        """Load the access token from the file."""
        try:
            with open(self._token_file, encoding='utf-8') as token_file:
                data = json.load(token_file)
        except IOError:
            return False
        self._token['access'] = data['token']
        if not self._token['access']:
            return False
        return True

    def store_access_token(self):
        """Store the access token to the file."""
        data = {'token': self.access_token}
        with open(self._token_file, 'w', encoding="utf-8") as token_file:
            json.dump(data, token_file)

    @handle_http_error
    def get_access_token(self, force=False, username=None, password=None):
        if self.load_access_token() and not force:
            return
        login_url = self.create_url('/login')
        click.echo(f'Login to {login_url}')
        username = username or click.prompt('Username')
        password = password or click.prompt('Password', hide_input=True)
        payload = {'username': username,
                   'password': password}
        response = requests.post(login_url, json=payload, timeout=30)
        response.raise_for_status()
        self._token['access'] = self.to_json(response)['token']
        self.store_access_token()
        logger.info('Login successful.')

    @handle_http_error
    @check_access_token
    def get_json(self, url, params=None):
        headers = {'Authorization': f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return self.to_json(response)

    @handle_http_error
    @check_access_token
    def put_json(self, url, params=None, payload=None):
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = requests.put(url, headers=headers, params=params, json=payload, timeout=30)
        logger.debug("PUT response: %s - %s", response, response.text)
        response.raise_for_status()
        return self.to_json(response)

    @handle_http_error
    @check_access_token
    def post_json(self, url, params=None, payload=None):
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = requests.post(url, headers=headers, params=params, json=payload, timeout=30)
        logger.debug("POST response: %s - %s", response, response.text)
        response.raise_for_status()
        return self.to_json(response)

    @handle_http_error
    @check_access_token
    def delete_json(self, url, params=None, payload=None):
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = requests.delete(url, headers=headers, params=params, json=payload, timeout=30)
        logger.debug("DELETE response: %s - %s", response, response.text)
        response.raise_for_status()
        return self.to_json(response)

    @staticmethod
    def to_json(response: requests.Response):
        try:
            return response.json()
        except Exception as e:
            logger.error('Expected valid json, but found %s', response.text)
            raise VjaError('Cannot parse json in response.') from e

    def get_user(self):
        return self.get_json(self.create_url('/user'))

    def get_namespaces(self):
        if self._cache['namespaces'] is None:
            self._cache['namespaces'] = self.get_json(self.create_url('/namespaces')) or []
        return self._cache['namespaces']

    def get_lists(self):
        if self._cache['lists'] is None:
            self._cache['lists'] = self.get_json(self.create_url('/lists')) or []
        return self._cache['lists']

    def get_list(self, list_id):
        return self.get_json(self.create_url(f'/lists/{str(list_id)}'))

    def put_list(self, namespace_id, title):
        payload = {'title': title}
        self.put_json(self.create_url(f'/namespaces/{str(namespace_id)}/lists'), payload=payload)

    def get_labels(self):
        if self._cache['labels'] is None:
            self._cache['labels'] = self.get_json(self.create_url('/labels')) or []
        return self._cache['labels']

    def put_label(self, title):
        payload = {'title': title}
        self.put_json(self.create_url('/labels'), payload=payload)

    def get_tasks(self, exclude_completed=True):
        if self._cache['tasks'] is None:
            url = self.create_url('/tasks/all')
            params = {'filter_by': 'done', 'filter_value': 'false'} if exclude_completed else None
            self._cache['tasks'] = self.get_json(url, params) or []
        return self._cache['tasks']

    def get_task(self, task_id):
        url = self.create_url(f'/tasks/{str(task_id)}')
        return self.get_json(url)

    def put_task(self, list_id, payload):
        return self.put_json(self.create_url(f'/lists/{str(list_id)}'), payload=payload)

    def post_task(self, task_id, payload):
        task_remote = self.get_task(task_id)
        task_remote.update(payload)
        return self.post_json(self.create_url(f'/tasks/{str(task_id)}'), payload=task_remote)

    def add_label_to_task(self, task_id, label_id):
        task_label_url = self.create_url(f'/tasks/{str(task_id)}/labels')
        payload = {'label_id': label_id}
        self.put_json(task_label_url, payload=payload)

    def remove_label_from_task(self, task_id, label_id):
        task_label_url = self.create_url(f'/tasks/{str(task_id)}/labels/{str(label_id)}')
        self.delete_json(task_label_url)

    def logout(self):
        if os.path.isfile(self._token_file):
            os.remove(self._token_file)
