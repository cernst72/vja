import logging

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
            raise VjaError(
                f"need access token to call function {func.__name__}; call authenticate()"
            ) from e

    return wrapper


def handle_http_error(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except requests.RequestException as error:
            # requests.RequestException is the base for all requests exceptions
            # including HTTPError, ConnectionError, Timeout, etc.
            # Handle HTTP errors (raised by response.raise_for_status()) specially
            if isinstance(error, requests.HTTPError):
                response = getattr(error, "response", None)
                url = getattr(response, "url", None)
                status = getattr(response, "status_code", None)
                if status == 401:
                    return _handle_http_401(self, response, func, args, kwargs)
                raise VjaError(
                    f"HTTP-Error {status}, url={url}, body={getattr(response, 'text', None)}"
                ) from error

            # Non-HTTP request exceptions (connection issues, timeouts, etc.)
            raise VjaError(f"Request failed: {error}") from error

    return wrapper


def _handle_http_401(self, response, func, args, kwargs):
    logger.debug(
        "Handle HTTP 401 error: %s", response.text
    )
    body_json = self.to_json(response)
    if body_json.get("code") == 11:
        # will only happen in vikunja > 2.0
        try:
            # try refresh first
            self.refresh_access_token()
            return func(self, *args, **kwargs)
        except (requests.RequestException, KeyError):
            # fallback to interactive login
            logger.info("Refresh failed or no refresh token; falling back to interactive login")
            self.authenticate(force_login=True)
            return func(self, *args, **kwargs)

    logger.info(
        "HTTP-Error 401, interactive login required...",
    )
    # force login and retry once
    self.authenticate(force_login=True)
    return func(self, *args, **kwargs)


class ApiClient:
    def __init__(self, api_url, token_file, oldapi):
        logger.debug("Connecting to api_url %s", api_url)
        self._api_url = api_url
        self._oldapi = oldapi
        self._cache = {"projects": None, "labels": None, "tasks": None}
        self._login = Login(api_url, token_file)

    @handle_http_error
    @inject_access_token
    def _get_json(self, url, params=None, headers=None):
        if params is None:
            params = {}
        response = requests.get(url, headers=headers, params=params, timeout=30)
        # too verbose:
        # logger.debug("GET response: %s - %s", response, response.text)
        response.raise_for_status()
        json_result = self.to_json(response)
        total_pages = int(response.headers.get("x-pagination-total-pages", 1))
        if total_pages > 1:
            logger.debug(
                "Trying to load all pages. Consider to increase MAXITEMSPERPAGE on your server instead."
            )
            for page in range(2, total_pages + 1):
                logger.debug("load page %s", page)
                params.update({"page": page})
                response = requests.get(url, headers=headers, params=params, timeout=30)
                response.raise_for_status()
                json_result = json_result + self.to_json(response)
        return json_result

    @handle_http_error
    @inject_access_token
    def _put_json(self, url, params=None, payload=None, headers=None):
        response = requests.put(
            url, headers=headers, params=params, json=payload, timeout=30
        )
        logger.debug("PUT response: %s - %s", response, response.text)
        response.raise_for_status()
        return self.to_json(response)

    @handle_http_error
    @inject_access_token
    def _post_json(self, url, params=None, payload=None, headers=None):
        response = requests.post(
            url, headers=headers, params=params, json=payload, timeout=30
        )
        logger.debug("POST response: %s - %s", response, response.text)
        response.raise_for_status()
        return self.to_json(response)

    @handle_http_error
    @inject_access_token
    def _delete_json(self, url, params=None, payload=None, headers=None):
        response = requests.delete(
            url, headers=headers, params=params, json=payload, timeout=30
        )
        logger.debug("DELETE response: %s - %s", response, response.text)
        response.raise_for_status()
        return self.to_json(response)

    @staticmethod
    def to_json(response: requests.Response):
        try:
            return response.json()
        except Exception as e:
            logger.error("Expected valid json, but found %s", response.text)
            raise VjaError("Cannot parse json in response.") from e

    def authenticate(
        self, force_login=True, username=None, password=None, totp_passcode=None
    ):
        try:
            self._login.validate_access_token(
                force_login, username, password, totp_passcode
            )
            return self._login.get_auth_header()
        except requests.HTTPError as error:
            raise VjaError(
                f"HTTP-Error {error.response.status_code}, url={error.response.url}, body={error.response.text}"
            ) from error

    def refresh_access_token(self):
        return self._login.refresh_access_token()

    def logout(self):
        self._login.logout()

    def get_user(self):
        return self._get_json(f"{self._api_url}/user")

    def get_projects(self):
        if self._cache["projects"] is None:
            self._cache["projects"] = self._get_json(f"{self._api_url}/projects") or []
        return self._cache["projects"]

    def get_project(self, project_id):
        return self._get_json(f"{self._api_url}/projects/{project_id}")

    def put_project(self, parent_project_id, title):
        payload = {"title": title, "parent_project_id": parent_project_id}
        return self._put_json(f"{self._api_url}/projects", payload=payload)

    def get_buckets(self, project_id, project_view_id):
        return self._get_json(
            f"{self._api_url}/projects/{project_id}/views/{project_view_id}/tasks"
        )

    def put_bucket(self, project_id, project_view_id, title):
        payload = {"title": title}
        return self._put_json(
            f"{self._api_url}/projects/{project_id}/views/{project_view_id}/buckets",
            payload=payload,
        )

    def get_labels(self):
        if self._cache["labels"] is None:
            self._cache["labels"] = self._get_json(f"{self._api_url}/labels") or []
        return self._cache["labels"]

    def put_label(self, title):
        payload = {"title": title}
        return self._put_json(f"{self._api_url}/labels", payload=payload)

    def get_tasks(self, exclude_completed=True):
        if self._cache["tasks"] is None:
            if self._oldapi:
                url = f"{self._api_url}/tasks/all"
            else:
                url = f"{self._api_url}/tasks"
            params = {"filter": "done=false"} if exclude_completed else {}
            self._cache["tasks"] = self._get_json(url, params) or []
        return self._cache["tasks"]

    def get_task(self, task_id):
        url = f"{self._api_url}/tasks/{task_id}"
        return self._get_json(url)

    def put_task(self, project_id, payload):
        return self._put_json(
            f"{self._api_url}/projects/{project_id}/tasks", payload=payload
        )

    def post_task(self, task_id, payload):
        return self._post_json(f"{self._api_url}/tasks/{task_id}", payload=payload)

    def delete_task(self, task_id):
        self._delete_json(f"{self._api_url}/tasks/{task_id}")

    def add_label_to_task(self, task_id, label_id):
        task_label_url = f"{self._api_url}/tasks/{task_id}/labels"
        payload = {"label_id": label_id}
        return self._put_json(task_label_url, payload=payload)

    def remove_label_from_task(self, task_id, label_id):
        task_label_url = f"{self._api_url}/tasks/{task_id}/labels/{label_id}"
        self._delete_json(task_label_url)
