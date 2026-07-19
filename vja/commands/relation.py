import click
from click_aliases import ClickAliasedGroup

from vja import VjaError
from vja.application import catch_exception, with_application
from vja.commands.task import task_show
from vja.model import RELATION_KINDS


@click.group(
    "relation",
    cls=ClickAliasedGroup,
    help="Subcommand: task relations (see help)",
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
