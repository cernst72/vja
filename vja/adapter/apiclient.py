import logging

import requests

from vja import VjaError
from vja.adapter.authenticate import Login
from vja.adapter.http_util import response_to_json

logger = logging.getLogger(__name__)


def inject_access_token(func):
    def wrapper(self, *args, **kwargs):
        headers = self.authenticate(force_login=False)
        return func(self, *args, headers=headers, **kwargs)

    return wrapper


def handle_http_error(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except requests.HTTPError as error:
            response = error.response
            if response.status_code == 401:
                return _handle_http_401(self, response, func, args, kwargs)
            msg = f"HTTP-Error {response.status_code}, url={response.url}, body={response.text}"
            raise VjaError(msg) from error
        except requests.RequestException as error:
            msg = f"Request failed: {error}"
            raise VjaError(msg) from error

    return wrapper


def _handle_http_401(client, response, func, args, kwargs):
    logger.debug("Handle HTTP 401 error: %s", response.text)
    body_json = response_to_json(response)
    if body_json.get("code") == 11:
        try:
            # try refresh first
            client.refresh_access_token()
            return func(client, *args, **kwargs)
        except (requests.RequestException, VjaError):
            # fallback to interactive login
            logger.info(
                "Refresh failed or no refresh token; falling back to interactive login"
            )
            client.authenticate(force_login=True)
            return func(client, *args, **kwargs)

    logger.info("HTTP-Error 401, interactive login required...")
    # force login and retry once
    client.authenticate(force_login=True)
    return func(client, *args, **kwargs)


class ApiClient:
    def __init__(self, api_url: str, token_file):
        logger.debug("Connecting to api_url %s", api_url)
        if "/v1" in api_url:
            raise VjaError(
                "Only v2 api is supported. Make sure Vikunja Server is >= 2.4.0 and configure api_url to /v2"
            )
        self._api_url = api_url
        self._cache = {"projects": None, "labels": None, "tasks": None}
        self._login = Login(self._api_url, token_file)

    @handle_http_error
    @inject_access_token
    def _get_json(self, url: str, params=None, headers=None):
        if params is None:
            params = {}
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        json_result = response_to_json(response)
        total_pages = int(json_result.get("total_pages", 1))
        if isinstance(json_result, dict) and "items" in json_result:
            json_result = json_result.get("items") or []
        if total_pages > 1:
            logger.debug(
                "Trying to load all pages. Consider to increase MAXITEMSPERPAGE on your server instead."
            )
            for page in range(2, total_pages + 1):
                logger.debug("load page %s", page)
                params["page"] = page
                response = requests.get(url, headers=headers, params=params, timeout=30)
                response.raise_for_status()
                page_result = response_to_json(response)
                if isinstance(page_result, dict) and "items" in page_result:
                    page_result = page_result.get("items") or []
                    json_result.extend(page_result)
        return json_result

    @handle_http_error
    @inject_access_token
    def _put_json(self, url: str, payload=None, headers=None):
        response = requests.put(url, headers=headers, json=payload, timeout=30)
        logger.debug("PUT response: %s - %s", response, response.text)
        response.raise_for_status()
        return response_to_json(response)

    @handle_http_error
    @inject_access_token
    def _post_json(self, url: str, payload=None, headers=None):
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        logger.debug("POST response: %s - %s", response, response.text)
        response.raise_for_status()
        return response_to_json(response)

    @handle_http_error
    @inject_access_token
    def _delete_json(self, url: str, payload=None, headers=None):
        response = requests.delete(url, headers=headers, json=payload, timeout=30)
        logger.debug("DELETE response: %s - %s", response, response.text)
        response.raise_for_status()
        return response_to_json(response)

    def authenticate(
        self, force_login=True, username=None, password=None, totp_passcode=None
    ):
        try:
            self._login.validate_access_token(
                force_login, username, password, totp_passcode
            )
            return self._login.get_auth_header()
        except requests.HTTPError as error:
            msg = f"HTTP-Error {error.response.status_code}, url={error.response.url}, body={error.response.text}"
            raise VjaError(msg) from error

    def refresh_access_token(self):
        return self._login.refresh_access_token()

    def logout(self):
        self._login.logout()

    def get_user(self) -> dict:
        return self._get_json(f"{self._api_url}/user")

    def get_projects(self) -> list[dict]:
        if self._cache["projects"] is None:
            self._cache["projects"] = self._get_json(f"{self._api_url}/projects") or []
        return self._cache["projects"]

    def get_project(self, project_id: int) -> dict:
        return self._get_json(f"{self._api_url}/projects/{project_id}")

    def create_project(self, title: str, parent_project_id: int | None) -> dict:
        payload = {"title": title, "parent_project_id": parent_project_id}
        return self._post_json(f"{self._api_url}/projects", payload=payload)

    def get_buckets(self, project_id: int, project_view_id: int) -> list[dict]:
        return self._get_json(
            f"{self._api_url}/projects/{project_id}/views/{project_view_id}/buckets"
        )

    def create_bucket(self, project_id: int, project_view_id: int, title: str) -> dict:
        payload = {"title": title}
        return self._post_json(
            f"{self._api_url}/projects/{project_id}/views/{project_view_id}/buckets",
            payload=payload,
        )

    def get_labels(self) -> list[dict]:
        if self._cache["labels"] is None:
            self._cache["labels"] = self._get_json(f"{self._api_url}/labels") or []
        return self._cache["labels"]

    def create_label(self, title: str) -> dict:
        payload = {"title": title}
        return self._post_json(f"{self._api_url}/labels", payload=payload)

    def get_tasks(self, exclude_completed: bool = True) -> list[dict]:
        if self._cache["tasks"] is None:
            url = f"{self._api_url}/tasks"
            params = {"filter": "done=false"} if exclude_completed else {}
            params["expand"] = "buckets"
            self._cache["tasks"] = self._get_json(url, params) or []
        return self._cache["tasks"]

    def get_task(self, task_id: int) -> dict:
        url = f"{self._api_url}/tasks/{task_id}"
        params = {"expand": "buckets"}
        return self._get_json(url, params)

    def create_task(self, project_id: int, payload: dict) -> dict:
        return self._post_json(
            f"{self._api_url}/projects/{project_id}/tasks", payload=payload
        )

    def update_task(self, task_id: int, payload: dict) -> dict:
        return self._put_json(f"{self._api_url}/tasks/{task_id}", payload=payload)

    def delete_task(self, task_id: int) -> None:
        self._delete_json(f"{self._api_url}/tasks/{task_id}")

    def add_label_to_task(self, task_id: int, label_id: int) -> dict:
        task_label_url = f"{self._api_url}/tasks/{task_id}/labels"
        payload = {"label_id": label_id}
        return self._post_json(task_label_url, payload=payload)

    def remove_label_from_task(self, task_id: int, label_id: int) -> None:
        task_label_url = f"{self._api_url}/tasks/{task_id}/labels/{label_id}"
        self._delete_json(task_label_url)

    def add_relation_to_task(
        self, task_id: int, relation_kind: str, other_task_id: int
    ) -> dict:
        task_relation_url = f"{self._api_url}/tasks/{task_id}/relations"
        payload = {"other_task_id": other_task_id, "relation_kind": relation_kind}
        return self._post_json(task_relation_url, payload=payload)

    def remove_relation_from_task(
        self, task_id: int, relation_kind: str, other_task_id: int
    ) -> None:
        task_relation_url = (
            f"{self._api_url}/tasks/{task_id}/relations/{relation_kind}/{other_task_id}"
        )
        self._delete_json(task_relation_url)

    def get_project_users(self, project_id: int)  -> list[dict]:
        return self._get_json(f"{self._api_url}/projects/{project_id}/users/search")

    def add_assignee_to_task(self, task_id: int, user_id: int) -> dict:
        payload = {"user_id": user_id}
        return self._post_json(
            f"{self._api_url}/tasks/{task_id}/assignees", payload=payload
        )

    def remove_assignee_from_task(self, task_id: int, user_id: int) -> None:
        self._delete_json(f"{self._api_url}/tasks/{task_id}/assignees/{user_id}")
