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


# relations
@cli.group(
    "relation",
    cls=ClickAliasedGroup,
    help="Subcommand: task relations (see help)",
    aliases=["relations"],
)
def relation_group():
    # vja relation
    pass


@relation_group.command(
    "add",
    help="Add a relation of the given KIND from TASK_ID to OTHER_TASK_ID "
    "(the inverse relation is created automatically by the server). "
    f"KIND is one of: {', '.join(RELATION_KINDS)}.",
)
@click.argument("task_id", required=True, type=click.INT)
@click.argument(
    "kind",
    required=True,
    metavar="KIND",
    type=click.Choice(RELATION_KINDS, case_sensitive=False),
)
@click.argument("other_task_id", required=True, type=click.INT)
@click.option(
    "quiet_show",
    "-q",
    "--quiet-show",
    "--quiet",
    is_flag=True,
    help="Hide confirmation message",
)
@click.option(
    "verbose_show",
    "-v",
    "--verbose-show",
    "--verbose",
    is_flag=True,
    help="Show resulting task when finished",
)
@with_application
@click.pass_context
@catch_exception(handle=VjaError)
def relation_add(
    ctx, application, task_id, kind, other_task_id, quiet_show=False, verbose_show=False
):
    task = application.command_service.add_relation(task_id, kind, other_task_id)
    if verbose_show or not quiet_show:
        click.echo(f"Modified task {task.id} in project {task.project.id}")
    if verbose_show:
        ctx.invoke(task_show, tasks=[task_id])


@relation_group.command(
    "remove",
    aliases=["rm", "delete"],
    help="Remove the relation of the given KIND between TASK_ID and OTHER_TASK_ID "
    "(the inverse relation is removed automatically by the server). "
    f"KIND is one of: {', '.join(RELATION_KINDS)}.",
)
@click.argument("task_id", required=True, type=click.INT)
@click.argument(
    "kind",
    required=True,
    metavar="KIND",
    type=click.Choice(RELATION_KINDS, case_sensitive=False),
)
@click.argument("other_task_id", required=True, type=click.INT)
@click.option(
    "quiet_show",
    "-q",
    "--quiet-show",
    "--quiet",
    is_flag=True,
    help="Hide confirmation message",
)
@click.option(
    "verbose_show",
    "-v",
    "--verbose-show",
    "--verbose",
    is_flag=True,
    help="Show resulting task when finished",
)
@with_application
@click.pass_context
@catch_exception(handle=VjaError)
def relation_remove(
    ctx, application, task_id, kind, other_task_id, quiet_show=False, verbose_show=False
):
    task = application.command_service.remove_relation(task_id, kind, other_task_id)
    if verbose_show or not quiet_show:
        click.echo(f"Modified task {task.id} in project {task.project.id}")
    if verbose_show:
        ctx.invoke(task_show, tasks=[task_id])


@cli.command("logout", help="Remove local access token")
@with_application
@catch_exception(handle=VjaError)
def logout(application):
    application.command_service.logout()


if __name__ == "__main__":
    cli()
