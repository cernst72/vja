#!/usr/bin/env python

import logging
import webbrowser
from functools import wraps, partial
from importlib import metadata

import click
from click_aliases import ClickAliasedGroup

from vja import VjaError
from vja.apiclient import ApiClient
from vja.config import VjaConfiguration
from vja.output import Output
from vja.project_service import ProjectService
from vja.service_command import CommandService
from vja.service_query import QueryService
from vja.task_service import TaskService
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
        api_client = ApiClient(self._configuration.get_api_url(), self._configuration.get_token_file())
        project_service = ProjectService(api_client)
        urgency_service = Urgency.from_config(self._configuration)
        task_service = TaskService(project_service, urgency_service)
        self._command_service = CommandService(project_service, task_service, api_client)
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
        url = self.configuration.get_frontend_url().rstrip('/')
        if task_id:
            url += f'/tasks/{str(task_id)}'
        webbrowser.open_new_tab(url)

    def open_browser_project(self, project_id):
        url = self.configuration.get_frontend_url().rstrip('/') + f'/projects/{str(project_id)}'
        webbrowser.open_new_tab(url)


with_application = click.make_pass_decorator(Application, ensure=True)


@click.group(cls=ClickAliasedGroup, context_settings={'help_option_names': ['-h', '--help']})
@click.pass_context
@click.version_option(metadata.version("vja"))
@click.option('-v', '--verbose', 'verbose', default=False, is_flag=True, help='Activate verbose logging')
@click.option('-u', '--username', 'username', help='Username for initial login (optional)')
@click.option('-p', '--password', 'password', help='Password for initial login (optional)')
@click.option('-t', '--totp-passcode', '--totp_passcode', 'totp_passcode',
              help='Time-based one-time passcode from your authenticator app (optional). '
                   'Only if TOTP is enabled on server.')
def cli(ctx=None, verbose=None, username=None, password=None, totp_passcode=None):
    if verbose:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(name)s: %(message)s')
        logger.debug(metadata.version("vja"))
    else:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger().setLevel(logging.INFO)
    application = Application()
    ctx.obj = application
    if username:
        application.command_service.login(username, password, totp_passcode)


# user
@cli.group('user', help='Subcommand: user (see help)')
def user_group():
    # vja user
    pass


@user_group.command('show', help='Print current user')
@click.option('is_json', '--json', default=False, is_flag=True, help='Print as Vikunja json')
@click.option('is_jsonvja', '--jsonvja', default=False, is_flag=True, help='Print as vja application json')
@with_application
@catch_exception(handle=VjaError)
def user_show(application, is_json=False, is_jsonvja=False):
    application.output.user(
        application.query_service.find_current_user(), is_json, is_jsonvja)


# projects
@cli.group('project', help='Subcommand: project (see help)', aliases=['projects'])
def project_group():
    # vja project
    pass


@project_group.command('add', help='Add project with title')
@click.option('parent_project', '-o', '--parent-project', '--parent_project',
              help='Create project as child of parent project. May be given by id or title of parent-project.')
@click.argument('title', nargs=-1, required=True)
@with_application
@catch_exception(handle=VjaError)
def project_add(application, title, parent_project=None):
    project = application.command_service.add_project(parent_project, " ".join(title))
    click.echo(f'Created project {project.id}')


@project_group.command('ls', help='Print projects ... (id; title; description; parent_project_id)')
@click.option('is_json', '--json', default=False, is_flag=True,
              help='Print as Vikunja json')
@click.option('is_jsonvja', '--jsonvja', default=False, is_flag=True,
              help='Print as vja application json')
@click.option('custom_format', '--custom-format',
              help='Format with template from .vjacli/vja.rc')
@with_application
@catch_exception(handle=VjaError)
def project_ls(application, is_json, is_jsonvja, custom_format):
    if custom_format:
        custom_format = application.configuration.get_custom_format_string(custom_format)
    application.output.project_array(
        application.query_service.find_all_projects(), is_json, is_jsonvja, custom_format)


@project_group.command('show', help='Show project details')
@click.argument('project_id', required=True, type=click.INT)
@click.option('is_json', '--json', default=False, is_flag=True,
              help='Print as Vikunja json')
@click.option('is_jsonvja', '--jsonvja', default=False, is_flag=True,
              help='Print as vja application json')
@with_application
@catch_exception(handle=VjaError)
def project_show(application, project_id, is_json, is_jsonvja):
    application.output.project(
        application.query_service.find_project_by_id(project_id), is_json, is_jsonvja)


@project_group.command('open', help='Open project in webbrowser')
@click.argument('project_id', required=True, type=click.INT)
@with_application
@catch_exception(handle=VjaError)
def project_open(application, project_id):
    application.open_browser_project(project_id)


# buckets
@cli.group('bucket', help='Subcommand: Kanban buckets (see help)', aliases=['buckets'])
def bucket_group():
    # vja bucket
    pass


@bucket_group.command('add',
                      help='Add bucket with title to the first Kanban View of the project')
@click.option('project', '-o', '--project', '--project-id',
              help='Create bucket in given project.')
@click.argument('title', nargs=-1, required=True)
@with_application
@catch_exception(handle=VjaError)
def bucket_add(application, title, project):
    bucket = application.command_service.add_bucket(project, " ".join(title))
    click.echo(f'Created bucket {bucket.id} in project {project}')


@bucket_group.command('ls',
                      help='Show Kanban buckets of given project (only the first Kanban View)... '
                           '(id; title; limit; count tasks)')
@click.option('project_id', '-o', '--project', '--project-id', '--project_id', required=True, type=click.INT,
              help='Show buckets of project with id')
@click.option('is_json', '--json', default=False, is_flag=True,
              help='Print as Vikunja json')
@click.option('is_jsonvja', '--jsonvja', default=False, is_flag=True,
              help='Print as vja application json')
@click.option('custom_format', '--custom-format',
              help='Format with template from .vjacli/vja.rc')
@with_application
@catch_exception(handle=VjaError)
def bucket_ls(application, project_id, is_json, is_jsonvja, custom_format):
    if custom_format:
        custom_format = application.configuration.get_custom_format_string(custom_format)
    application.output.bucket_array(
        application.query_service.find_buckets_in_first_kanban_view(project_id), is_json, is_jsonvja, custom_format)


# labels
@cli.group('label', help='Subcommand: label (see help)', aliases=['labels'])
def label_group():
    # vja label
    pass


@label_group.command('ls', help='Print labels ... (id; title)')
@click.option('is_json', '--json', default=False, is_flag=True,
              help='Print as Vikunja json')
@click.option('is_jsonvja', '--jsonvja', default=False, is_flag=True,
              help='Print as vja application json')
@click.option('custom_format', '--custom-format',
              help='Format with template from .vjacli/vja.rc')
@with_application
@catch_exception(handle=VjaError)
def label_ls(application, is_json, is_jsonvja, custom_format):
    if custom_format:
        custom_format = application.configuration.get_custom_format_string(custom_format)
    application.output.label_array(
        application.query_service.find_all_labels(), is_json, is_jsonvja, custom_format)


@label_group.command('add', help='Add label with title')
@click.argument('title', required=True, nargs=-1)
@with_application
@catch_exception(handle=VjaError)
def label_add(application, title):
    label = application.command_service.add_label(" ".join(title))
    click.echo(f'Created label {label.id}')


# tasks
@cli.command('add', aliases=['create'],
             help='Add new task')
@click.argument('title', required=True, nargs=-1)
@click.option('quiet_show', '-q', '--quiet-show', '--quiet', is_flag=True,
              help='Hide confirmation message')
@click.option('verbose_show', '-v', '--verbose-show', '--verbose', is_flag=True,
              help='Show resulting task when finished')
@click.option('project_id', '-o', '--project', '--project-id', '--project_id',
              help='Project (id or name), defaults to project from user settings, than to first favorite project')
@click.option('note', '-n', '--note', '--notes', '--description',
              help='Set description (note)')
@click.option('prio', '-p', '--prio', '--priority',
              help='Set priority')
@click.option('due', '-d', '--due', '--duedate', '--due-date', '--due_date',
              help='Set due date (supports parsedatetime expressions)')
@click.option('favorite', '-f', '--star', '--favorite', type=click.BOOL, is_flag=True,
              help='Mark as favorite')
@click.option('label', '-l', '--label', multiple=True,
              help='Set label (label must exist on server)')
@click.option('reminder', '-r', '--alarm', '--remind', '--reminder', is_flag=False, flag_value='due',
              help='Set reminder (supports parsedatetime and timedelta expressions). '
                   'Absolute: "in 3 days at 18:00" or relative: "1h before due_date" or just -r to set equal to '
                   'due date.')
@click.option('force_create', '--force-create', '--force', is_flag=True,
              help='Force creation of non existing label')
@with_application
@click.pass_context
@catch_exception(handle=VjaError)
def task_add(ctx, application, title, quiet_show=False, verbose_show=False, **args):
    args_present = {k: v for k, v in args.items() if v is not None}
    task = application.command_service.add_task(" ".join(title), args_present.copy())
    if verbose_show or not quiet_show:
        click.echo(f'Created task {task.id} in project {task.project.id}')
    if verbose_show:
        ctx.invoke(task_show, tasks=[task.id])


@cli.command('clone', aliases=['copy'],
             help='Clone task with given task_id. Set the new title')
@click.argument('task_id', required=True, type=click.INT)
@click.argument('title', required=True, nargs=-1)
@click.option('quiet_show', '-q', '--quiet-show', '--quiet', is_flag=True,
              help='Hide confirmation message')
@click.option('verbose_show', '-v', '--verbose-show', '--verbose', is_flag=True,
              help='Show resulting task when finished')
@with_application
@click.pass_context
@catch_exception(handle=VjaError)
def task_clone(ctx, application, task_id, title, quiet_show=False, verbose_show=False):
    task = application.command_service.clone_task(task_id, " ".join(title))
    if verbose_show or not quiet_show:
        click.echo(f'Created task {task.id} in project {task.project.id} as clone from {task_id}')
    if verbose_show:
        ctx.invoke(task_show, tasks=[task.id])


@cli.command('edit', aliases=['modify', 'update'],
             help='Modify task/tasks. (Opens task in browser if no options are given)')
@click.argument('task_ids', required=True, type=click.INT, nargs=-1)
@click.option('quiet_show', '-q', '--quiet-show', '--quiet', is_flag=True,
              help='Hide confirmation message')
@click.option('verbose_show', '-v', '--verbose-show', '--verbose', is_flag=True,
              help='Show resulting task when finished')
@click.option('title', '-i', '--title',
              help='Set title')
@click.option('note', '-n', '--note', '--notes', '--description',
              help='Set description (note)')
@click.option('note_append', '-a', '--note-append', '--append-note', '--description-append', '--append-description',
              help='Append note to existing description separated by new line')
@click.option('prio', '-p', '--prio', '--priority', type=click.INT,
              help='Set priority')
@click.option('project_id', '-o', '--project', '--project-id', '--project_id',
              help='Move to project with id')
@click.option('position', '--project-position', '--project_position', '--position', type=click.INT,
              help='Set project position')
@click.option('bucket_id', '--bucket-id', '--bucket_id', type=click.INT,
              help='Set bucket id')
@click.option('kanban_position', '--kanban-position', '--kanban_position', type=click.INT,
              help='Set kanban position')
@click.option('due', '-d', '--due', '--duedate', '--due-date', '--due_date',
              help='Set due date (supports parsedatetime expressions)')
@click.option('favorite', '-f/ ', '--favorite/--no-favorite', '--star/--no-star', is_flag=True, default=None,
              help='Mark or unmark task as favorite')
@click.option('completed', '-c', '--completed', '--done', type=click.BOOL,
              help='Mark as completed')
@click.option('label', '-l', '--label',
              help='Set label (label must exist on server unless called with --force-create)')
@click.option('reminder', '-r', '--alarm', '--remind', '--reminder', is_flag=False, flag_value='due',
              help='Set reminder (supports parsedatetime and timedelta expressions). '
                   'Absolute: "in 3 days at 18:00" or relative: "1h30m before due_date" or just -r to set equal to '
                   'due date.')
@click.option('force_create', '--force-create', '--force', is_flag=True, default=None,
              help='Force creation of non existing label')
@with_application
@click.pass_context
@catch_exception(handle=VjaError)
def task_edit(ctx, application, task_ids, quiet_show=False, verbose_show=False, **args):
    args_present = {k: v for k, v in args.items() if v is not None}
    for task_id in task_ids:
        if args_present:
            task = application.command_service.edit_task(task_id, args_present.copy())
            if verbose_show or not quiet_show:
                click.echo(f'Modified task {task.id} in project {task.project.id}')
            if verbose_show:
                ctx.invoke(task_show, tasks=[task.id])
        else:
            application.open_browser_task(task_id)


@cli.command('toggle', aliases=['check', 'click', 'done'], help='Shortcut for marking / unmarking task as done')
@click.argument('task_id', required=True, type=click.INT)
@click.option('quiet_show', '-q', '--quiet-show', '--quiet', is_flag=True,
              help='Hide confirmation message')
@click.option('verbose_show', '-v', '--verbose-show', '--verbose', is_flag=True,
              help='Show resulting task when finished')
@with_application
@click.pass_context
@catch_exception(handle=VjaError)
def task_toggle(ctx, application, task_id, quiet_show=False, verbose_show=False):
    task = application.command_service.toggle_task_done(task_id)
    if verbose_show or not quiet_show:
        click.echo(f'Modified task {task.id} in project {task.project.id}')
    if verbose_show:
        ctx.invoke(task_show, tasks=[task_id])


@cli.command('defer', aliases=['delay'], help='Shortcut for moving the due_date and the reminders of the task. '
                                              'Examples for valid delay values are 2d, 1h30m.')
@click.argument('task_ids', required=True, type=click.INT, nargs=-1)
@click.argument('delay_by', required=True)
@click.option('quiet_show', '-q', '--quiet-show', '--quiet', is_flag=True,
              help='Hide confirmation message')
@click.option('verbose_show', '-v', '--verbose-show', '--verbose', is_flag=True,
              help='Show resulting task when finished')
@with_application
@click.pass_context
@catch_exception(handle=VjaError)
def task_defer(ctx, application, task_ids, delay_by, quiet_show=False, verbose_show=False):
    for task_id in task_ids:
        task = application.command_service.defer_task(task_id, delay_by)
        if verbose_show or not quiet_show:
            click.echo(f'Modified task {task.id} in project {task.project.id}')
        if verbose_show:
            ctx.invoke(task_show, tasks=[task_id])


@cli.command('ls', help='List tasks ... (task-id; priority; is_favorite; title; due_date; '
                        'has reminder; parent-project; project; labels; urgency). '
                        'Optionally limit output to given TASK_IDs.')
@click.argument('task_ids', type=click.INT, nargs=-1)
@click.option('is_json', '--json', default=False, is_flag=True,
              help='Print as Vikunja json')
@click.option('is_jsonvja', '--jsonvja', default=False, is_flag=True,
              help='Print as vja application json')
@click.option('custom_format', '--custom-format',
              help='Format with template from .vjacli/vja.rc')
@click.option('sort_string', '--sort', '--sort-by', '--sort-string',
              help='Sort by arguments (Arguments are task attributes separated by ",") '
                   '(Prefix each criteria with "-" to reverse order')
@click.option('include_completed', '--include-completed', '--all', default=False, is_flag=True,
              help='Include completed tasks')
@click.option('due_date_filter', '-d', '--due', '--due-date', '--due_date',
              help='Filter by due date. The TEXT value must be like <operator> <value> '
                   'Shortcut for --filter="due_date <operator> <value>"')
@click.option('favorite_filter', '-f', '--favorite', '--star', type=click.BOOL,
              help='Filter by favorite flag. Shortcut for --filter="favorite_filter eq <value>"')
@click.option('general_filter', '--filter', multiple=True,
              help='General filter. Must be like <field> <operator> <value> e.g. --filter="priority ge 2" '
                   'where <operator> in (eq, ne, gt, lt, ge, le, before, after, contains). '
                   'Multiple occurrences of --filter are allowed and will be combined with logical AND.')
@click.option('label_filter', '-l', '--label',
              help='Filter by label (regex or id)')
@click.option('project_filter', '-o', '--project', '--project-id', '--project_id',
              help='Filter by project (regex or id)')
@click.option('upper_project_filter', '-t', '--base-project', '--top', '--base', '--upper-project',
              help='Filter by base project (regex or id). '
                   'All tasks whose project has the given argument as a ancestor are considered.')
@click.option('priority_filter', '-p', '--prio', '--priority',
              help='Filter by priority. The TEXT value must be like <operator> <value>, '
                   'Shortcut for --filter="priority <operator> <value>"')
@click.option('title_filter', '-i', '--title',
              help='Filter title (regex)')
@click.option('urgency_filter', '-u', '--urgent', '--urgency', is_flag=False, flag_value=4, type=click.INT,
              help='Filter by minimum urgency.  Shortcut for --filter="urgency ge <value>"')
@with_application
@catch_exception(handle=VjaError)
def task_ls(application, task_ids, is_json, is_jsonvja, custom_format, include_completed, sort_string=None,
            **filter_args):
    if custom_format:
        custom_format = application.configuration.get_custom_format_string(custom_format)
    filter_args = {k: v for k, v in filter_args.items() if v is not None}

    tasks = application.query_service.find_filtered_tasks(include_completed, sort_string, filter_args)
    if task_ids:
        tasks = [t for t in tasks if t.id in task_ids]

    application.output.task_array(tasks, is_json, is_jsonvja, custom_format)
    if not is_json and not is_jsonvja and not custom_format:
        click.echo(f"Count: {len(list(tasks))}")


@cli.command('show', help='Show task details. Multiple task ids may be given')
@click.argument('tasks', type=click.INT, nargs=-1)
@click.option('is_json', '--json', default=False, is_flag=True,
              help='Print as Vikunja json')
@click.option('is_jsonvja', '--jsonvja', default=False, is_flag=True,
              help='Print as vja application json')
@with_application
@catch_exception(handle=VjaError)
def task_show(application, tasks, is_json, is_jsonvja):
    for task_id in tasks:
        task = application.query_service.find_task_by_id(task_id)
        application.output.task(task, is_json, is_jsonvja)


@cli.command(name='open', help='Open task in browser. Multiple task ids may be given. '
                               'If tasks is empty, then open vikunjas starting page.')
@click.argument('tasks', required=False, type=click.INT, nargs=-1)
@with_application
@catch_exception(handle=VjaError)
def task_open(application, tasks):
    if not tasks:
        application.open_browser_task('')
    else:
        for task_id in tasks:
            application.open_browser_task(task_id)


# task group
@cli.group('task', help='(optional) subcommand: task (see help)', aliases=['tasks'])
def task_group():
    # vja task
    pass


task_group.add_command(task_add)
task_group.add_command(task_clone)
task_group.add_command(task_edit)
task_group.add_command(task_toggle)
task_group.add_command(task_defer)
task_group.add_command(task_ls)
task_group.add_command(task_show)
task_group.add_command(task_open)


@cli.command('logout', help='Remove local access token')
@with_application
@catch_exception(handle=VjaError)
def logout(application):
    application.command_service.logout()


if __name__ == '__main__':
    cli()
