import webbrowser
from functools import partial, wraps

import click

from vja import VjaError
from vja.adapter.apiclient import ApiClient
from vja.config import VjaConfiguration
from vja.output import Output
from vja.service.project_service import ProjectService
from vja.service.service_command import CommandService
from vja.service.service_query import QueryService
from vja.service.task_service import TaskService
from vja.urgency import Urgency


def catch_exception(func=None, *, handle):
    if not func:
        return partial(catch_exception, handle=handle)

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except handle as e:
            raise click.ClickException(e)

    return wrapper


class Application:
    @catch_exception(handle=VjaError)
    def __init__(self):
        self._configuration = VjaConfiguration()
        api_client = ApiClient(
            self._configuration.get_api_url(), self._configuration.get_token_file()
        )
        project_service = ProjectService(api_client)
        urgency_service = Urgency.from_config(self._configuration)
        task_service = TaskService(project_service, urgency_service)
        self._command_service = CommandService(
            project_service, task_service, api_client
        )
        self._query_service = QueryService(project_service, task_service, api_client)
        self._output = Output()

    @property
    def command_service(self) -> CommandService:
        return self._command_service

    @property
    def query_service(self) -> QueryService:
        return self._query_service

    @property
    def output(self) -> Output:
        return self._output

    @property
    def configuration(self) -> VjaConfiguration:
        return self._configuration

    def open_browser_task(self, task_id):
        url = self.configuration.get_frontend_url().rstrip("/")
        if task_id:
            url += f"/tasks/{str(task_id)}"
        webbrowser.open_new_tab(url)

    def open_browser_project(self, project_id):
        url = (
            self.configuration.get_frontend_url().rstrip("/")
            + f"/projects/{str(project_id)}"
        )
        webbrowser.open_new_tab(url)


with_application = click.make_pass_decorator(Application, ensure=True)
