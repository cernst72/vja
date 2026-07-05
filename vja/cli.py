#!/usr/bin/env python

import logging
import webbrowser
from functools import wraps, partial
from importlib import metadata

import click
from click_aliases import ClickAliasedGroup

from vja import VjaError
from vja.adapter.apiclient import ApiClient
from vja.config import VjaConfiguration
from vja.output import Output
from vja.service.project_service import ProjectService
from vja.service.service_command import CommandService
from vja.service.service_query import QueryService
from vja.service.task_service import TaskService
from vja.urgency import Urgency

logger = logging.getLogger(__name__)


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


@click.group(
    cls=ClickAliasedGroup, context_settings={"help_option_names": ["-h", "--help"]}
)
@click.pass_context
@click.version_option(metadata.version("vja"))
@click.option(
    "-v",
    "--verbose",
    "verbose",
    default=False,
    is_flag=True,
    help="Activate verbose logging",
)
@click.option(
    "-u", "--username", "username", help="Username for initial login (optional)"
)
@click.option(
    "-p", "--password", "password", help="Password for initial login (optional)"
)
@click.option(
    "-t",
    "--totp-passcode",
    "--totp_passcode",
    "totp_passcode",
    help="Time-based one-time passcode from your authenticator app (optional). "
    "Only if TOTP is enabled on server.",
)
def cli(ctx=None, verbose=None, username=None, password=None, totp_passcode=None):
    if verbose:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        )
        logger.debug(metadata.version("vja"))
    else:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger().setLevel(logging.INFO)
    application = Application()
    ctx.obj = application
    if username:
        application.command_service.login(username, password, totp_passcode)


# user
from vja.commands import user as user_module # noqa
cli.add_command(user_module.user_group)

from vja.commands import project as projects_module # noqa
cli.add_command(projects_module.project_group, aliases=["projects"])

from vja.commands import bucket as buckets_module # noqa
cli.add_command(buckets_module.bucket_group, aliases=["buckets"])

from vja.commands import label as labels_module # noqa
cli.add_command(labels_module.label_group, aliases=["labels"])

from vja.commands import task as tasks_module # noqa
cli.add_command(tasks_module.task_group, aliases=["tasks"])

# shortcuts for vja task commands
cli.add_command(tasks_module.task_add, aliases=["create"])
cli.add_command(tasks_module.task_clone, aliases=["copy"])
cli.add_command(tasks_module.task_edit, aliases=["modify", "update"])
cli.add_command(tasks_module.task_toggle, aliases=["check", "click", "done"])
cli.add_command(tasks_module.task_defer, aliases=["delay"])
cli.add_command(tasks_module.task_delete, aliases=["rm", "remove"])
cli.add_command(tasks_module.task_ls)
cli.add_command(tasks_module.task_show)
cli.add_command(tasks_module.task_open)


@cli.command("logout", help="Remove local access token")
@with_application
@catch_exception(handle=VjaError)
def logout(application):
    application.command_service.logout()


if __name__ == "__main__":
    cli()
