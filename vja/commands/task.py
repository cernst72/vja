import click
from click_aliases import ClickAliasedGroup

from vja import VjaError
from vja.application import Application, catch_exception, with_application


@click.group(
    "task", help="(optional) subcommand: task (see help)", cls=ClickAliasedGroup
)
def task_group():
    # vja task
    pass


@task_group.command("add", help="Add new task", aliases=["create"])
@click.argument("title", required=True, nargs=-1)
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
@click.option(
    "project_id",
    "-o",
    "--project",
    "--project-id",
    "--project_id",
    help="Project (id or title), defaults to project from user settings, then to first favorite project",
)
@click.option(
    "note", "-n", "--note", "--notes", "--description", help="Set description (note)"
)
@click.option("prio", "-p", "--prio", "--priority", help="Set priority")
@click.option(
    "due",
    "-d",
    "--due",
    "--duedate",
    "--due-date",
    "--due_date",
    help="Set due date (supports parsedatetime expressions)",
)
@click.option(
    "--start",
    "--start-date",
    "--start_date",
    help="Set start date (supports parsedatetime expressions)",
)
@click.option(
    "--end",
    "--end-date",
    "--end_date",
    help="Set end date (supports parsedatetime expressions)",
)
@click.option(
    "favorite",
    "-f",
    "--star",
    "--favorite",
    type=click.BOOL,
    is_flag=True,
    help="Mark as favorite",
)
@click.option(
    "label",
    "-l",
    "--label",
    multiple=True,
    help="Set label (label must exist on server)",
)
@click.option(
    "assignee",
    "-A",
    "--assignee",
    multiple=True,
    help="Assign task to user (username)",
)
@click.option(
    "reminder",
    "-r",
    "--alarm",
    "--remind",
    "--reminder",
    is_flag=False,
    flag_value="due",
    help="Set reminder (supports parsedatetime and timedelta expressions). "
    'Absolute: "in 3 days at 18:00" or relative: "1h before due_date" or just -r to set equal to '
    "due date.",
)
@click.option(
    "force_create",
    "--force-create",
    "--force",
    is_flag=True,
    help="Force creation of non existing label",
)
@with_application
@click.pass_context
@catch_exception(handle=VjaError)
def task_add(
    ctx: click.Context,
    application: Application,
    title,
    quiet_show=False,
    verbose_show=False,
    **args,
):
    args_present = {k: v for k, v in args.items() if v is not None}
    task = application.command_service.add_task(" ".join(title), args_present.copy())
    if verbose_show or not quiet_show:
        click.echo(f"Created task {task.id} in project {task.project.id}")
    if verbose_show:
        ctx.invoke(task_show, tasks=[task.id])


@task_group.command(
    "clone", help="Clone task with given task_id. Set the new title", aliases=["copy"]
)
@click.argument("task_id", required=True, type=click.INT)
@click.argument("title", required=True, nargs=-1)
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
def task_clone(
    ctx: click.Context,
    application: Application,
    task_id,
    title,
    quiet_show=False,
    verbose_show=False,
):
    task = application.command_service.clone_task(task_id, " ".join(title))
    if verbose_show or not quiet_show:
        click.echo(
            f"Created task {task.id} in project {task.project.id} as clone from {task_id}"
        )
    if verbose_show:
        ctx.invoke(task_show, tasks=[task.id])


@task_group.command(
    "edit",
    aliases=["modify", "update"],
    help="Modify task/tasks. (Opens task in browser if no options are given)",
)
@click.argument("task_ids", required=True, type=click.INT, nargs=-1)
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
@click.option("title", "-i", "--title", help="Set title")
@click.option(
    "note", "-n", "--note", "--notes", "--description", help="Set description (note)"
)
@click.option(
    "note_append",
    "-a",
    "--note-append",
    "--append-note",
    "--description-append",
    "--append-description",
    help="Append note to existing description separated by new line",
)
@click.option("prio", "-p", "--prio", "--priority", type=click.INT, help="Set priority")
@click.option(
    "project_id",
    "-o",
    "--project",
    "--project-id",
    "--project_id",
    help="Move to project (id or title)",
)
@click.option(
    "position",
    "--project-position",
    "--project_position",
    "--position",
    type=click.INT,
    help="Set project position",
)
@click.option(
    "bucket_id", "--bucket-id", "--bucket_id", type=click.INT, help="Set bucket id"
)
@click.option(
    "kanban_position",
    "--kanban-position",
    "--kanban_position",
    type=click.INT,
    help="Set kanban position",
)
@click.option(
    "due",
    "-d",
    "--due",
    "--duedate",
    "--due-date",
    "--due_date",
    help="Set due date (supports parsedatetime expressions)",
)
@click.option(
    "--start",
    "--start-date",
    "--start_date",
    help="Set start date (supports parsedatetime expressions)",
)
@click.option(
    "--end",
    "--end-date",
    "--end_date",
    help="Set end date (supports parsedatetime expressions)",
)
@click.option(
    "favorite",
    "-f/--no-favorite",
    "--star/--no-star",
    is_flag=True,
    default=None,
    help="Mark or unmark task as favorite",
)
@click.option(
    "completed",
    "-c",
    "--completed",
    "--done",
    type=click.BOOL,
    help="Mark as completed",
)
@click.option(
    "label",
    "-l",
    "--label",
    help="Set label (label must exist on server unless called with --force-create)",
)
@click.option(
    "assignee",
    "-A",
    "--assignee",
    help="Toggle assignee (username): adds if not assigned, removes if already assigned",
)
@click.option(
    "reminder",
    "-r",
    "--alarm",
    "--remind",
    "--reminder",
    is_flag=False,
    flag_value="due",
    help="Set reminder (supports parsedatetime and timedelta expressions). "
    'Absolute: "in 3 days at 18:00" or relative: "1h30m before due_date" or just -r to set equal to '
    "due date.",
)
@click.option(
    "force_create",
    "--force-create",
    "--force",
    is_flag=True,
    default=None,
    help="Force creation of non existing label",
)
@with_application
@click.pass_context
@catch_exception(handle=VjaError)
def task_edit(
    ctx: click.Context,
    application: Application,
    task_ids,
    quiet_show=False,
    verbose_show=False,
    **args,
):
    args_present = {k: v for k, v in args.items() if v is not None}
    for task_id in task_ids:
        if args_present:
            task = application.command_service.edit_task(task_id, args_present.copy())
            if verbose_show or not quiet_show:
                click.echo(f"Modified task {task.id} in project {task.project.id}")
            if verbose_show:
                ctx.invoke(task_show, tasks=[task.id])
        else:
            application.open_browser_task(task_id)


@task_group.command(
    "toggle",
    help="Shortcut for marking / unmarking task as done",
)
@click.argument("task_id", required=True, type=click.INT)
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
def task_toggle(
    ctx: click.Context,
    application: Application,
    task_id,
    quiet_show=False,
    verbose_show=False,
):
    task = application.command_service.toggle_task_done(task_id)
    if verbose_show or not quiet_show:
        click.echo(f"Modified task {task.id} in project {task.project.id}")
    if verbose_show:
        ctx.invoke(task_show, tasks=[task_id])


@task_group.command(
    "defer",
    help="Shortcut for moving the due_date and the reminders of the task. "
    "Examples for valid delay values are 2d, 1h30m.",
)
@click.argument("task_ids", required=True, type=click.INT, nargs=-1)
@click.argument("delay_by", required=True)
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
def task_defer(
    ctx: click.Context,
    application: Application,
    task_ids,
    delay_by,
    quiet_show=False,
    verbose_show=False,
):
    for task_id in task_ids:
        task = application.command_service.defer_task(task_id, delay_by)
        if verbose_show or not quiet_show:
            click.echo(f"Modified task {task.id} in project {task.project.id}")
        if verbose_show:
            ctx.invoke(task_show, tasks=[task_id])


@task_group.command(
    "delete",
    help="Delete task/tasks permanently.",
)
@click.argument("task_ids", required=True, type=click.INT, nargs=-1)
@click.option(
    "quiet_show",
    "-q",
    "--quiet-show",
    "--quiet",
    is_flag=True,
    help="Hide confirmation message",
)
@with_application
@catch_exception(handle=VjaError)
def task_delete(application: Application, task_ids, quiet_show=False):
    for task_id in task_ids:
        application.command_service.delete_task(task_id)
        if not quiet_show:
            click.echo(f"Deleted task {task_id}")


@task_group.command(
    "ls",
    aliases=["list"],
    help="List tasks ... (task-id; priority; is_favorite; title; due_date; "
    "has reminder; parent-project; project; labels; urgency). "
    "Optionally limit output to given TASK_IDs.",
)
@click.argument("task_ids", type=click.INT, nargs=-1)
@click.option(
    "is_json", "--json", default=False, is_flag=True, help="Print as Vikunja json"
)
@click.option(
    "is_jsonvja",
    "--jsonvja",
    default=False,
    is_flag=True,
    help="Print as vja application json",
)
@click.option(
    "custom_format", "--custom-format", help="Format with template from .vjacli/vja.rc"
)
@click.option(
    "sort_string",
    "--sort",
    "--sort-by",
    "--sort-string",
    help='Sort by arguments (Arguments are task attributes separated by ",") '
    '(Prefix each criteria with "-" to reverse order',
)
@click.option(
    "include_completed",
    "--include-completed",
    "--all",
    default=False,
    is_flag=True,
    help="Include completed tasks",
)
@click.option(
    "due_date_filter",
    "-d",
    "--due",
    "--due-date",
    "--due_date",
    help="Filter by due date. The TEXT value must be like <operator> <value> "
    'Shortcut for --filter="due_date <operator> <value>"',
)
@click.option(
    "favorite_filter",
    "-f",
    "--favorite",
    "--star",
    type=click.BOOL,
    help='Filter by favorite flag. Shortcut for --filter="favorite_filter eq <value>"',
)
@click.option(
    "general_filter",
    "--filter",
    multiple=True,
    help='General filter. Must be like <field> <operator> <value> e.g. --filter="priority ge 2" '
    "where <operator> in (eq, ne, gt, lt, ge, le, before, after, contains). "
    "Multiple occurrences of --filter are allowed and will be combined with logical AND.",
)
@click.option("label_filter", "-l", "--label", help="Filter by label (id or title-regex)")
@click.option(
    "project_filter",
    "-o",
    "--project",
    "--project-id",
    "--project_id",
    help="Filter by project (id or title-regex)",
)
@click.option(
    "upper_project_filter",
    "-t",
    "--base-project",
    "--top",
    "--base",
    "--upper-project",
    help="Filter by base project (regex or id). "
    "All tasks whose project has the given argument as a ancestor are considered.",
)
@click.option(
    "priority_filter",
    "-p",
    "--prio",
    "--priority",
    help="Filter by priority. The TEXT value must be like <operator> <value>, "
    'Shortcut for --filter="priority <operator> <value>"',
)
@click.option("title_filter", "-i", "--title", help="Filter title (regex)")
@click.option(
    "urgency_filter",
    "-u",
    "--urgent",
    "--urgency",
    is_flag=False,
    flag_value=4,
    type=click.INT,
    help='Filter by minimum urgency.  Shortcut for --filter="urgency ge <value>"',
)
@click.option(
    "verbose_ls",
    "-v",
    "--verbose-ls",
    "--verbose",
    is_flag=True,
    help="Show count of tasks",
)
@with_application
@catch_exception(handle=VjaError)
def task_ls(
    application: Application,
    task_ids,
    is_json,
    is_jsonvja,
    custom_format,
    include_completed,
    sort_string=None,
    verbose_ls=False,
    **filter_args,
):
    if custom_format:
        custom_format = application.configuration.get_custom_format_string(
            custom_format
        )
    filter_args = {k: v for k, v in filter_args.items() if v is not None}

    tasks = application.query_service.find_filtered_tasks(
        include_completed, sort_string, filter_args
    )
    if task_ids:
        tasks = [t for t in tasks if t.id in task_ids]

    application.output.task_array(tasks, is_json, is_jsonvja, custom_format)
    if verbose_ls:
        click.echo(f"Count: {len(list(tasks))}")


@task_group.command("show", help="Show task details. Multiple task ids may be given")
@click.argument("tasks", type=click.INT, nargs=-1)
@click.option(
    "is_json", "--json", default=False, is_flag=True, help="Print as Vikunja json"
)
@click.option(
    "is_jsonvja",
    "--jsonvja",
    default=False,
    is_flag=True,
    help="Print as vja application json",
)
@with_application
@catch_exception(handle=VjaError)
def task_show(application: Application, tasks, is_json, is_jsonvja):
    for task_id in tasks:
        task = application.query_service.find_task_by_id(task_id)
        application.output.task(task, is_json, is_jsonvja)


@task_group.command(
    name="open",
    help="Open task in browser. Multiple task ids may be given. "
    "If tasks is empty, then open vikunjas starting page.",
)
@click.argument("tasks", required=False, type=click.INT, nargs=-1)
@with_application
@catch_exception(handle=VjaError)
def task_open(application: Application, tasks):
    if not tasks:
        application.open_browser_task("")
    else:
        for task_id in tasks:
            application.open_browser_task(task_id)
