#!/usr/bin/env python

import logging
import webbrowser
from importlib import metadata

import click
from click_aliases import ClickAliasedGroup

from vja.apiclient import ApiClient
from vja.config import VjaConfiguration
from vja.list_service import ListService
from vja.output import Output
from vja.service_command import CommandService
from vja.service_query import QueryService
from vja.task_service import TaskService
from vja.urgency import Urgency

logger = logging.getLogger(__name__)


class Application:
    def __init__(self):
        self._configuration = VjaConfiguration()
        api_client = ApiClient(self._configuration.get_api_url(), self._configuration.get_token_file())
        list_service = ListService(api_client)
        urgency_service = Urgency.from_config(self._configuration)
        task_service = TaskService(list_service, urgency_service)
        self._command_service = CommandService(list_service, task_service, api_client)
        self._query_service = QueryService(list_service, task_service, api_client)
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

    def open_browser(self, task):
        url = self.configuration.get_frontend_url().rstrip('/')
        if task:
            url += f'/tasks/{str(task)}'
        webbrowser.open_new_tab(url)


with_application = click.make_pass_decorator(Application, ensure=True)


@click.group(cls=ClickAliasedGroup, context_settings=dict({'help_option_names': ['-h', '--help']}))
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
        logging.basicConfig(level=logging.DEBUG)
        logger.debug('Verbose mode on')
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
    pass


@user_group.command('show', help='Print current user')
@click.option('is_json', '--json', default=False, is_flag=True, help='Print as Vikunja json')
@click.option('is_jsonvja', '--jsonvja', default=False, is_flag=True, help='Print as vja application json')
@with_application
def user_show(application, is_json=False, is_jsonvja=False):
    application.output.user(
        application.query_service.find_current_user(), is_json, is_jsonvja)


# projects
@cli.group('project', help='Subcommand: project (see help)')
def project_group():
    pass


@project_group.command('add', help='Add project with title')
@click.option('namespace_id', '-n', '--namespace-id', help='Create project in namespace, default: first namespace found')
@click.argument('title', nargs=-1, required=True)
@with_application
def project_add(application, title, namespace_id=None):
    project = application.command_service.add_project(namespace_id, " ".join(title))
    click.echo(f'Created project {project.id}')


@project_group.command('ls', help='Print projects ... (id; title; description; namespace; namespace_id)')
@click.option('is_json', '--json', default=False, is_flag=True,
              help='Print as Vikunja json')
@click.option('is_jsonvja', '--jsonvja', default=False, is_flag=True,
              help='Print as vja application json')
@click.option('custom_format', '--custom-format',
              help='Format with template from .vjacli/vja.rc')
@with_application
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
def project_show(application, project_id, is_json, is_jsonvja):
    application.output.project(
        application.query_service.find_project_by_id(project_id), is_json, is_jsonvja)


# buckets
@cli.group('bucket', help='Subcommand: kanban buckets (see help)')
def bucket_group():
    pass


@bucket_group.command('ls', help='Print kanban buckets of given project ... (id; title; is_done; limit; count tasks)')
@click.option('project_id', '-l', '--list', '--project-id', '--project_id', required=True, type=click.INT,
              help='Show buckets of project with id')
@click.option('is_json', '--json', default=False, is_flag=True,
              help='Print as Vikunja json')
@click.option('is_jsonvja', '--jsonvja', default=False, is_flag=True,
              help='Print as vja application json')
@click.option('custom_format', '--custom-format',
              help='Format with template from .vjacli/vja.rc')
@with_application
def bucket_ls(application, project_id, is_json, is_jsonvja, custom_format):
    if custom_format:
        custom_format = application.configuration.get_custom_format_string(custom_format)
    application.output.bucket_array(
        application.query_service.find_all_buckets_in_project(project_id), is_json, is_jsonvja, custom_format)


# labels
@cli.group('label', help='Subcommand: label (see help)')
def label_group():
    pass


@label_group.command('ls', help='Print labels ... (id; title)')
@click.option('is_json', '--json', default=False, is_flag=True,
              help='Print as Vikunja json')
@click.option('is_jsonvja', '--jsonvja', default=False, is_flag=True,
              help='Print as vja application json')
@click.option('custom_format', '--custom-format',
              help='Format with template from .vjacli/vja.rc')
@with_application
def label_ls(application, is_json, is_jsonvja, custom_format):
    if custom_format:
        custom_format = application.configuration.get_custom_format_string(custom_format)
    application.output.label_array(
        application.query_service.find_all_labels(), is_json, is_jsonvja, custom_format)


@label_group.command('add', help='Add label with title')
@click.argument('title', required=True, nargs=-1)
@with_application
def label_add(application, title):
    label = application.command_service.add_label(" ".join(title))
    click.echo(f'Created label {label.id}')


# tasks
@cli.command('add', aliases=['create'],
             help='Add new task')
@click.argument('title', required=True, nargs=-1)
@click.option('project_id', '-l', '--folder', '--project', '--list',
              help='Project (id or name), defaults to project from user settings, than to first favorite project')
@click.option('note', '-n', '--note', '--description',
              help='Set description (note)')
@click.option('prio', '-p', '--prio', '--priority',
              help='Set priority')
@click.option('due', '-d', '--due', '--duedate', '--due-date', '--due_date',
              help='Set due date (supports parsedatetime expressions)')
@click.option('favorite', '-f', '--star', '--favorite', type=click.BOOL,
              help='Mark as favorite')
@click.option('tag', '-t', '--tag', '--label',
              help='Set label (label must exist on server)')
@click.option('reminder', '-r', '--alarm', '--remind', '--reminder', is_flag=False, flag_value='due',
              help='Set reminder (supports parsedatetime and timedelta expressions). '
                   'Absolute: "in 3 days at 18:00" or relative: "1h before due_date" or just -r to set equal to '
                   'due date.')
@click.option('force_create', '--force-create', '--force', is_flag=True,
              help='Force creation of non existing label')
@with_application
@click.pass_context
def task_add(ctx, application, title, **args):
    args_present = {k: v for k, v in args.items() if v is not None}
    task = application.command_service.add_task(" ".join(title), args_present.copy())
    click.echo(f'Created task {task.id} in project {task.project.id}')
    ctx.invoke(task_show, tasks=[task.id])


@cli.command('clone', aliases=['copy'],
             help='Clone task with given task_id. Set the new title')
@click.argument('task_id', required=True, type=click.INT)
@click.argument('title', required=True, nargs=-1)
@with_application
@click.pass_context
def task_clone(ctx, application, task_id, title):
    task = application.command_service.clone_task(task_id, " ".join(title))
    click.echo(f'Created task {task.id} in project {task.project.id} as clone from {task_id}')
    ctx.invoke(task_show, tasks=[task.id])


@cli.command('edit', aliases=['modify', 'update'],
             help='Modify task/tasks. (Opens task in browser if no options are given)')
@click.argument('task_ids', required=True, type=click.INT, nargs=-1)
@click.option('title', '-i', '--title',
              help='Set title')
@click.option('note', '-n', '--note', '--description',
              help='Set description (note)')
@click.option('note_append', '-a', '--note-append', '--append-note', '--description-append', '--append-description',
              help='Append note to existing description separated by new line')
@click.option('prio', '-p', '--prio', '--priority', type=click.INT,
              help='Set priority')
@click.option('project_id', '-l', '--folder-id', '--project-id', '--list-id', '--project_id', type=click.INT,
              help='Move to project with id')
@click.option('position', '--project-position', '--project_position', '--position', type=click.INT,
              help='Set project position')
@click.option('bucket_id', '--bucket-id', '--bucket_id', type=click.INT,
              help='Set bucket id')
@click.option('kanban_position', '--kanban-position', '--kanban_position', type=click.INT,
              help='Set kanban position')
@click.option('due', '-d', '--due', '--duedate', '--due-date', '--due_date',
              help='Set due date (supports parsedatetime expressions)')
@click.option('favorite', '-f', '--favorite', '--star', type=click.BOOL,
              help='Mark as favorite')
@click.option('completed', '-c', '--completed', '--done', type=click.BOOL,
              help='Mark as completed')
@click.option('tag', '-t', '--tag', '--label',
              help='Set label (label must exist on server unless called with --force-create)')
@click.option('reminder', '-r', '--alarm', '--remind', '--reminder', is_flag=False, flag_value='due',
              help='Set reminder (supports parsedatetime and timedelta expressions). '
                   'Absolute: "in 3 days at 18:00" or relative: "1h30m before due_date" or just -r to set equal to '
                   'due date.')
@click.option('force_create', '--force-create', '--force', is_flag=True, default=None,
              help='Force creation of non existing label')
@with_application
@click.pass_context
def task_edit(ctx, application, task_ids, **args):
    args_present = {k: v for k, v in args.items() if v is not None}
    for task_id in task_ids:
        if args_present:
            task = application.command_service.edit_task(task_id, args_present.copy())
            click.echo(f'Modified task {task.id} in project {task.project.id}')
            ctx.invoke(task_show, tasks=[task.id])
        else:
            application.open_browser(task_id)


@cli.command('toggle', aliases=['check', 'click', 'done'], help='Shortcut for marking / unmarking task as done')
@click.argument('task_id', required=True, type=click.INT)
@with_application
@click.pass_context
def task_toggle(ctx, application, task_id):
    task = application.command_service.toggle_task_done(task_id)
    click.echo(f'Modified task {task.id} in project {task.project.id}')
    ctx.invoke(task_show, tasks=[task_id])


@cli.command('defer', aliases=['delay'], help='Shortcut for moving the due_date and the reminders of the task. '
                                              'Examples for valid delay values are 2d, 1h30m.')
@click.argument('task_ids', required=True, type=click.INT, nargs=-1)
@click.argument('delay_by', required=True)
@with_application
@click.pass_context
def task_defer(ctx, application, task_ids, delay_by):
    for task_id in task_ids:
        task = application.command_service.defer_task(task_id, delay_by)
        click.echo(f'Modified task {task.id} in project {task.project.id}')
        ctx.invoke(task_show, tasks=[task_id])


@cli.command('ls', help='List tasks ... (task-id; priority; is_favorite; title; due_date; '
                        'has reminder; namespace; project; labels; urgency)')
@click.option('is_json', '--json', default=False, is_flag=True,
              help='Print as Vikunja json')
@click.option('is_jsonvja', '--jsonvja', default=False, is_flag=True,
              help='Print as vja application json')
@click.option('custom_format', '--custom-format',
              help='Format with template from .vjacli/vja.rc')
@click.option('sort_string', '--sort', '--sort-by', '--sort-string',
              help='Sort by arguments (Arguments ar task attributes separated by ",") '
                   '(Prefix each criteria with "-" to reverse order')
@click.option('include_completed', '--include-completed', default=False, is_flag=True,
              help='Include completed tasks')
@click.option('bucket_filter', '-b', '--bucket', '--bucket-id', '--bucket_id',
              help='Filter by kanban bucket id. Shortcut for --filter="bucket_id eq <value>".')
@click.option('due_date_filter', '-d', '--due', '--due-date', '--due_date',
              help='Filter by due date. The TEXT value must be like <operator> <value> '
                   'Shortcut for --filter="due_date <operator> <value>"')
@click.option('favorite_filter', '-f', '--favorite', '--star', type=click.BOOL,
              help='Filter by favorite flag. Shortcut for --filter="favorite_filter eq <value>"')
@click.option('general_filter', '--filter', multiple=True,
              help='General filter. Must be like <field> <operator> <value> e.g. --filter="priority ge 2" '
                   'where <operator> in (eq, ne, gt, lt, ge, le, before, after, contains). '
                   'Multiple occurrences of --filter are allowed and will be combined with logical AND.')
@click.option('label_filter', '-t', '--tag', '--label',
              help='Filter by label (name or id)')
@click.option('project_filter', '-l', '--project',
              help='Filter by project (name or id)')
@click.option('namespace_filter', '-n', '--namespace',
              help='Filter by namespace (name or id)')
@click.option('priority_filter', '-p', '--prio', '--priority',
              help='Filter by priority. The TEXT value must be like <operator> <value>, '
                   'Shortcut for --filter="priority <operator> <value>"')
@click.option('title_filter', '-i', '--title',
              help='Filter title (regex)')
@click.option('urgency_filter', '-u', '--urgency', is_flag=False, flag_value=3, type=click.INT,
              help='Filter by minimum urgency.  Shortcut for --filter="urgency ge <value>"')
@with_application
def task_ls(application, is_json, is_jsonvja, custom_format, include_completed, sort_string=None, **filter_args):
    if custom_format:
        custom_format = application.configuration.get_custom_format_string(custom_format)
    filter_args = {k: v for k, v in filter_args.items() if v is not None}

    tasks = application.query_service.find_filtered_tasks(include_completed, sort_string, filter_args)
    application.output.task_array(tasks, is_json, is_jsonvja, custom_format)


@cli.command('show', help='Show task details. Multiple task ids may be given')
@click.argument('tasks', type=click.INT, nargs=-1)
@click.option('is_json', '--json', default=False, is_flag=True,
              help='Print as Vikunja json')
@click.option('is_jsonvja', '--jsonvja', default=False, is_flag=True,
              help='Print as vja application json')
@with_application
def task_show(application, tasks, is_json, is_jsonvja):
    for task_id in tasks:
        task = application.query_service.find_task_by_id(task_id)
        application.output.task(task, is_json, is_jsonvja)


@cli.command(name='open', help='Open task in browser')
@click.argument('task', required=False, type=click.INT)
@with_application
def task_open(application, task):
    application.open_browser(task)


@cli.command('logout', help='Remove local access token')
@with_application
def logout(application):
    application.command_service.logout()


if __name__ == '__main__':
    cli()
