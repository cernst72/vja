import logging
import sys

import requests

from vja import VjaError
from vja.authenticate import Login

logger = logging.getLogger(__name__)


def inject_access_token(func):
    def wrapper(self, *args, **kwargs):
        try:
            headers = self.authenticate(force_login=False)
            return func(self, headers=headers, *args, **kwargs)
        except KeyError as e:
            raise VjaError(f'need access token to call function {func.__name__}; call authenticate()') from e

    return wrapper


def handle_http_error(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except requests.HTTPError as error:
            if error.response.status_code == 401:
                logger.info('HTTP-Error %s, url=%s; trying to retrieve new access token...',
                            error.response.status_code, error.response.url)
                self.authenticate(force_login=True)
                return func(self, *args, **kwargs)
            logger.warning('HTTP-Error %s, url=%s, body=%s',
                           error.response.status_code, error.response.url, error.response.text)
            sys.exit(1)

    return wrapper


class ApiClient:
    def __init__(self, api_url, token_file):
        logger.debug('Connecting to api_url %s', api_url)
        self._api_url = api_url
        self._cache = {'lists': None, 'labels': None, 'namespaces': None, 'tasks': None}
        self._login = Login(api_url, token_file)

    def _create_url(self, path):
        return self._api_url + path

    @handle_http_error
    @inject_access_token
    def _get_json(self, url, params=None, headers=None):
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        json_result = self._to_json(response)
        total_pages = int(response.headers.get('x-pagination-total-pages', 1))
        if total_pages > 1:
            logger.debug('Trying to load all pages. Consider to increase MAXITEMSPERPAGE on your server instead.')
            for page in range(2, total_pages + 1):
                logger.debug('load page %s', page)
                params.update({'page': page})
                response = requests.get(url, headers=headers, params=params, timeout=30)
                response.raise_for_status()
                json_result = json_result + self._to_json(response)
        return json_result

    @handle_http_error
    @inject_access_token
    def _put_json(self, url, params=None, payload=None, headers=None):
        response = requests.put(url, headers=headers, params=params, json=payload, timeout=30)
        logger.debug("PUT response: %s - %s", response, response.text)
        response.raise_for_status()
        return self._to_json(response)

    @handle_http_error
    @inject_access_token
    def _post_json(self, url, params=None, payload=None, headers=None):
        response = requests.post(url, headers=headers, params=params, json=payload, timeout=30)
        logger.debug("POST response: %s - %s", response, response.text)
        response.raise_for_status()
        return self._to_json(response)

    @handle_http_error
    @inject_access_token
    def _delete_json(self, url, params=None, payload=None, headers=None):
        response = requests.delete(url, headers=headers, params=params, json=payload, timeout=30)
        logger.debug("DELETE response: %s - %s", response, response.text)
        response.raise_for_status()
        return self._to_json(response)

    @staticmethod
    def _to_json(response: requests.Response):
        try:
            return response.json()
        except Exception as e:
            logger.error('Expected valid json, but found %s', response.text)
            raise VjaError('Cannot parse json in response.') from e

    def authenticate(self, force_login=True, username=None, password=None, totp_passcode=None):
        try:
            self._login.validate_access_token(force_login, username, password, totp_passcode)
            return self._login.get_auth_header()
        except requests.HTTPError as error:
            logger.warning('HTTP-Error %s, url=%s, body=%s',
                           error.response.status_code, error.response.url, error.response.text)
            sys.exit(1)

    def logout(self):
        self._login.logout()

    def get_user(self):
        return self._get_json(self._create_url('/user'))

    def get_namespaces(self):
        if self._cache['namespaces'] is None:
            self._cache['namespaces'] = self._get_json(self._create_url('/namespaces')) or []
        return self._cache['namespaces']

    def get_lists(self):
        if self._cache['lists'] is None:
            self._cache['lists'] = self._get_json(self._create_url('/lists')) or []
        return self._cache['lists']

    def get_list(self, list_id):
        return self._get_json(self._create_url(f'/lists/{str(list_id)}'))

    def put_list(self, namespace_id, title):
        payload = {'title': title}
        return self._put_json(self._create_url(f'/namespaces/{str(namespace_id)}/lists'), payload=payload)

    def get_buckets(self, list_id):
        return self._get_json(self._create_url(f'/lists/{str(list_id)}/buckets'))

    def get_labels(self):
        if self._cache['labels'] is None:
            self._cache['labels'] = self._get_json(self._create_url('/labels')) or []
        return self._cache['labels']

    def put_label(self, title):
        payload = {'title': title}
        return self._put_json(self._create_url('/labels'), payload=payload)

    def get_tasks(self, exclude_completed=True):
        if self._cache['tasks'] is None:
            url = self._create_url('/tasks/all')
            params = {'filter_by': 'done', 'filter_value': 'false'} if exclude_completed else None
            self._cache['tasks'] = self._get_json(url, params) or []
        return self._cache['tasks']

    def get_task(self, task_id):
        url = self._create_url(f'/tasks/{str(task_id)}')
        return self._get_json(url)

    def put_task(self, list_id, payload):
        return self._put_json(self._create_url(f'/lists/{str(list_id)}'), payload=payload)

    def post_task(self, task_id, payload):
        return self._post_json(self._create_url(f'/tasks/{str(task_id)}'), payload=payload)

    def add_label_to_task(self, task_id, label_id):
        task_label_url = self._create_url(f'/tasks/{str(task_id)}/labels')
        payload = {'label_id': label_id}
        return self._put_json(task_label_url, payload=payload)

    def remove_label_from_task(self, task_id, label_id):
        task_label_url = self._create_url(f'/tasks/{str(task_id)}/labels/{str(label_id)}')
        self._delete_json(task_label_url)
