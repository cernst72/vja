#!/usr/bin/env python

import logging
from importlib import metadata

import click
from click_aliases import ClickAliasedGroup

from vja import VjaError
from vja.application import Application, catch_exception, with_application
from vja.commands import bucket as buckets_module
from vja.commands import label as labels_module
from vja.commands import project as projects_module
from vja.commands import task as tasks_module
from vja.commands import user as user_module

logger = logging.getLogger(__name__)


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
def cli(
    ctx: click.Context, verbose=None, username=None, password=None, totp_passcode=None
):
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


cli.add_command(user_module.user_group)
cli.add_command(projects_module.project_group, aliases=["projects"])
cli.add_command(buckets_module.bucket_group, aliases=["buckets"])
cli.add_command(labels_module.label_group, aliases=["labels"])
cli.add_command(tasks_module.task_group, aliases=["tasks"])

# shortcuts for vja task commands
cli.add_command(tasks_module.task_add, aliases=["create"])
cli.add_command(tasks_module.task_clone, aliases=["copy"])
cli.add_command(tasks_module.task_edit, aliases=["modify", "update"])
cli.add_command(tasks_module.task_toggle, aliases=["check", "click", "done"])
cli.add_command(tasks_module.task_defer, aliases=["delay"])
cli.add_command(tasks_module.task_delete, aliases=["rm", "remove"])
cli.add_command(tasks_module.task_ls, aliases=["list"])
cli.add_command(tasks_module.task_show)
cli.add_command(tasks_module.task_open)


@cli.command("logout", help="Remove local access token")
@with_application
@catch_exception(handle=VjaError)
def logout(application):
    application.command_service.logout()


if __name__ == "__main__":
    cli()
