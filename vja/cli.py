#!/usr/bin/env python

import logging
import webbrowser
from importlib import metadata

import click
from click_aliases import ClickAliasedGroup

from vja.apiclient import ApiClient
from vja.config import VjaConfiguration
from vja.list_service import ListService
from vja.service_command import CommandService
from vja.service_query import QueryService

logger = logging.getLogger(__name__)


class Application:
    def __init__(self):
        self._configuration = VjaConfiguration()
        api_client = ApiClient(self.configuration.get_api_url(), self._configuration.get_token_file())
        list_service = ListService(api_client)
        self._command_service = CommandService(list_service, api_client)
        self._query_service = QueryService(list_service, api_client)

    @property
    def command_service(self):
        return self._command_service

    @property
    def query_service(self):
        return self._query_service

    @property
    def configuration(self):
        return self._configuration

    def open_browser(self, task):
        url = self.configuration.get_frontend_url()
        if task and task > 0:
            url += f'/tasks/{str(task)}'
        webbrowser.open_new_tab(url)


with_application = click.make_pass_decorator(Application, ensure=True)


@click.group(cls=ClickAliasedGroup, context_settings=dict(help_option_names=['-h', '--help']))
@click.pass_context
@click.version_option(metadata.version("vja"))
@click.option('-v', '--verbose', 'verbose', default=False, is_flag=True, help='verbose output')
@click.option('-u', '--username', 'username', help='username for initial login (optional)')
@click.option('-p', '--password', 'password', help='password for initial login (optional)')
def cli(ctx=None, verbose=None, username=None, password=None):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
        logger.debug('Verbose mode on')
    else:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger().setLevel(logging.INFO)
    application = Application()
    ctx.obj = application
    if username or password:
        application.command_service.authenticate(username, password)


# user
@cli.group('user', help='subcommand: user (see help)')
def user_group():
    pass


@user_group.command('show', help='print current user')
@click.option('is_json', '--json', default=False, is_flag=True, help='print as Vikunja json')
@click.option('is_jsonvja', '--jsonvja', default=False, is_flag=True, help='print as vja application json')
@with_application
def user_show(application, is_json=False, is_jsonvja=False):
    application.query_service.print_user(is_json, is_jsonvja)


# namespaces
@cli.group('namespace', help='subcommand: namespace (see help)')
def namespace_group():
    pass


@namespace_group.command('ls', help='print namespaces')
@click.option('is_json', '--json', default=False, is_flag=True, help='print as Vikunja json')
@click.option('is_jsonvja', '--jsonvja', default=False, is_flag=True, help='print as vja application json')
@with_application
def namespace_ls(application, is_json=False, is_jsonvja=False):
    application.query_service.print_namespaces(is_json, is_jsonvja)


# lists
@cli.group('list', help='subcommand: list (see help)')
def list_group():
    pass


@list_group.command('add', help='add list with title')
@click.option('namespace_id', '-n', '--namespace-id', help='create list in namespace, default: first list found')
@click.argument('title', nargs=-1, required=True)
@with_application
def list_add(application, title, namespace_id=None):
    tasklist = application.command_service.add_list(namespace_id, " ".join(title))
    click.echo(f'Created list {tasklist.id}')


@list_group.command('ls', help='print lists')
@click.option('is_json', '--json', default=False, is_flag=True, help='print as Vikunja json')
@click.option('is_jsonvja', '--jsonvja', default=False, is_flag=True, help='print as vja application json')
@with_application
def list_ls(application, is_json, is_jsonvja):
    application.query_service.print_lists(is_json, is_jsonvja)


@list_group.command('show', help='show list details')
@click.argument('list_id', required=True, type=click.INT)
@click.option('is_json', '--json', default=False, is_flag=True, help='print as Vikunja json')
@click.option('is_jsonvja', '--jsonvja', default=False, is_flag=True, help='print as vja application json')
@with_application
def list_show(application, list_id, is_json, is_jsonvja):
    application.query_service.print_list(list_id, is_json, is_jsonvja)


# buckets
@cli.group('bucket', help='subcommand: kanban buckets (see help)')
def bucket_group():
    pass


@bucket_group.command('ls', help='print kanban buckets')
@click.option('list_id', '-l', '--list', '--list-id', '--list_id', required=True, type=click.INT,
              help='show buckets in list with id')
@click.option('is_json', '--json', default=False, is_flag=True, help='print as Vikunja json')
@click.option('is_jsonvja', '--jsonvja', default=False, is_flag=True, help='print as vja application json')
@with_application
def bucket_ls(application, list_id, is_json, is_jsonvja):
    application.query_service.print_buckets(list_id, is_json, is_jsonvja)


# labels
@cli.group('label', help='subcommand: label (see help)')
def label_group():
    pass


@label_group.command('ls', help='print labels')
@click.option('is_json', '--json', default=False, is_flag=True, help='print as Vikunja json')
@click.option('is_jsonvja', '--jsonvja', default=False, is_flag=True, help='print as vja application json')
@with_application
def label_ls(application, is_json, is_jsonvja):
    application.query_service.print_labels(is_json, is_jsonvja)


@label_group.command('add', help='add label with title')
@click.argument('title', required=True, nargs=-1)
@with_application
def label_add(application, title):
    label = application.command_service.add_label(" ".join(title))
    click.echo(f'Created label {label.id}')


# tasks
@cli.command('add', help='add new task')
@click.argument('title', required=True, nargs=-1)
@click.option('list_id', '-l', '--folder', '--project', '--list',
              help='list (id or name), default: first favorite list')
@click.option('note', '-n', '--note', '--description', help='set description (note)')
@click.option('prio', '-p', '--prio', '--priority', help='set priority')
@click.option('due', '-d', '--due', '--duedate', '--due-date', '--due_date',
              help='set due date (supports parsedatetime expressions)')
@click.option('favorite', '-f', '--star', '--favorite', type=click.BOOL, help='mark as favorite')
@click.option('tag', '-t', '--tag', '--label', help='set label (label must exist on server)')
@click.option('reminder', '-r', '--alarm', '--remind', '--reminder', is_flag=False, flag_value='due',
              help='set reminder (supports parsedatetime expressions)')
@click.option('force_create', '--force-create', '--force', is_flag=True, help='force creation of non existing label')
@with_application
@click.pass_context
def task_add(ctx, application, title, **args):
    task = application.command_service.add_task(" ".join(title), {k: v for k, v in args.items() if v is not None})
    click.echo(f'Created task {task.id} in list {task.tasklist.id}')
    ctx.invoke(task_show, tasks=[task.id])


@cli.command('edit', aliases=['modify', 'update'],
             help='modify task/tasks (opens task in browser if no options are given)')
@click.argument('task_ids', required=True, type=click.INT, nargs=-1)
@click.option('title', '-i', '--title', help='set title')
@click.option('note', '-n', '--note', '--description', help='set description (note)')
@click.option('prio', '-p', '--prio', '--priority', type=click.INT, help='set priority')
@click.option('position', '--position', type=click.INT, help='set list position')
@click.option('bucket_id', '--bucket-id', '--bucket_id', type=click.INT, help='set bucket id')
@click.option('kanban_position', '--kanban-position', '--kanban_position', type=click.INT, help='set kanban position')
@click.option('due', '-d', '--due', '--duedate', '--due-date', help='set due date (supports parsedatetime expressions)')
@click.option('favorite', '-f', '--favorite', '--star', type=click.BOOL, help='mark as favorite')
@click.option('completed', '-c', '--completed', '--done', type=click.BOOL, help='mark as completed')
@click.option('tag', '-t', '--tag', '--label', help='set label (label must exist on server)')
@click.option('reminder', '-r', '--alarm', '--remind', '--reminder', is_flag=False, flag_value='due',
              help='set reminder (supports parsedatetime expressions)')
@click.option('force_create', '--force-create', '--force', is_flag=True, help='force creation of non existing label')
@with_application
@click.pass_context
def task_edit(ctx, application, task_ids, **args):
    args_present = {k: v for k, v in args.items() if v is not None}
    for task_id in task_ids:
        if not args_present:
            application.open_browser(task_id)
        else:
            task = application.command_service.edit_task(task_id, args_present)
            click.echo(f'Modified task {task.id} in list {task.tasklist.id}')
            ctx.invoke(task_show, tasks=[task.id])


@cli.command('toggle', aliases=['check', 'click', 'done'], help='shortcut for marking / unmarking task as done')
@click.argument('task_id', required=True, type=click.INT)
@with_application
@click.pass_context
def task_toggle(ctx, application, task_id):
    task = application.command_service.toggle_task_done(task_id)
    click.echo(f'Modified task {task.id} in list {task.tasklist.id}')
    ctx.invoke(task_show, tasks=[task_id])


@cli.command('ls', help='list tasks')
@click.option('is_json', '--json', default=False, is_flag=True, help='print as Vikunja json')
@click.option('is_jsonvja', '--jsonvja', default=False, is_flag=True, help='print as vja application json')
@click.option('include_completed', '--include-completed', default=False, is_flag=True, help='include completed tasks')
@click.option('namespace_filter', '-n', '--namespace', help='filter by namespace (name or id)')
@click.option('list_filter', '-l', '--list', help='filter by list (name or id)')
@click.option('label_filter', '-t', '--label', '--tag', help='filter by label (name or id)')
@click.option('favorite_filter', '-f', '--favorite', '--star', type=click.BOOL, help='filter by favorite flag')
@click.option('title_filter', '-i', '--title', help='filter title (regex)')
@click.option('urgency_filter', '-u', '--urgency', is_flag=False, flag_value=3, type=click.INT,
              help='filter by urgency at least')
@with_application
def task_ls(application,
            is_json, is_jsonvja, include_completed, namespace_filter, list_filter, label_filter, favorite_filter,
            title_filter, urgency_filter):
    application.query_service.print_tasks(is_json, is_jsonvja, include_completed, namespace_filter, list_filter,
                                          label_filter, favorite_filter, title_filter, urgency_filter)


@cli.command('show', help='show task details. Multiple task ids may be given')
@click.argument('tasks', type=click.INT, nargs=-1)
@click.option('is_json', '--json', default=False, is_flag=True, help='print as Vikunja json')
@click.option('is_jsonvja', '--jsonvja', default=False, is_flag=True, help='print as vja application json')
@with_application
def task_show(application, tasks, is_json, is_jsonvja):
    for task in tasks:
        application.query_service.print_task(task, is_json, is_jsonvja)


@cli.command(name='open', help='open task in browser')
@click.argument('task', required=False, type=click.INT)
@with_application
def task_open(application, task):
    application.open_browser(task)


@cli.command('logout', help='remove local access token')
@with_application
def logout(application):
    application.command_service.logout()


if __name__ == '__main__':
    cli()
