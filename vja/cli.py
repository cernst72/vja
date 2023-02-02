#!/usr/bin/env python

import logging
import webbrowser
from importlib import metadata

import click
from click_aliases import ClickAliasedGroup

from vja import config, service

logger = logging.getLogger(__name__)


@click.group(cls=ClickAliasedGroup)
@click.version_option(metadata.version("vja"))
@click.option('-v', '--verbose', 'verbose', default=False, is_flag=True, help='verbose output')
@click.option('-u', '--username', 'username', help='username for initial login (optional)')
@click.option('-p', '--password', 'password', help='password for initial login (optional)')
def cli(verbose=None, username=None, password=None):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
        logger.debug('Verbose mode on')
    else:
        logging.basicConfig(level=logging.INFO)
    if username or password:
        service.authenticate(username, password)


@cli.command('help')
@click.argument('subcommand')
@click.pass_context
def help_command(ctx, subcommand):
    subcommand_obj = cli.get_command(ctx, subcommand)
    if subcommand_obj is None:
        click.echo("I don't know that command.")
    else:
        click.echo(subcommand_obj.get_help(ctx))


# namespaces
@cli.group('namespace', help='subcommand: namespace (see help)')
def namespace_group():
    pass


@namespace_group.command('ls', help='print namespaces')
def namespace_ls():
    service.print_namespaces()


# lists
@cli.group('list', help='subcommand: list (see help)')
def list_group():
    pass


@list_group.command('add', help='add list with title')
@click.option('namespace_id', '-n', '--namespace-id', help='create list in namespace, default: first list found')
@click.argument('title', nargs=-1, required=True)
def list_add(title, namespace_id=None):
    service.add_list(namespace_id, " ".join(title))


@list_group.command('ls', help='print lists')
def list_ls():
    service.print_lists()


@list_group.command('show', help='show list details')
@click.argument('list_id', required=True, type=click.INT)
def list_show(list_id):
    service.print_list(list_id)


# labels
@cli.group('label', help='subcommand: label (see help)')
def label_group():
    pass


@label_group.command('ls', help='print labels')
def label_ls():
    service.print_labels()


@label_group.command('add', help='add label with title')
@click.argument('title', required=True, nargs=-1)
def label_add(title):
    service.add_label(" ".join(title))


# tasks
@cli.command('add', help='add new task')
@click.argument('title', required=True, nargs=-1)
@click.option('list_id', '-l', '--list', '--folder', type=click.INT, help='list index, default: first favorite list')
@click.option('note', '-n', '--note', '--description', help='set description (note)')
@click.option('prio', '-p', '--prio', '--priority', help='set priority')
@click.option('due', '-d', '--due', '--duedate', '--due-date', help='set due date (uses parsedatetime to parse)')
@click.option('favorite', '-f', '--favorite', '--star', type=click.BOOL, help='mark as favorite')
@click.option('tag', '-t', '--tag', '--label', help='set tag (tag must exist on server)')
@click.option('reminder', '-r', '--reminder', '--alarm', help='set reminder (uses parsedatetime)')
def task_add(title, **args):
    service.add_task(" ".join(title), {k: v for k, v in args.items() if v is not None})


@cli.command('edit', aliases=['modify', 'update'], help='modify task (opens browser if no options are given)')
@click.argument('task_id', required=True, type=click.INT)
@click.option('title', '-i', '--title', help='set title')
@click.option('note', '-n', '--note', '--description', help='set description (note)')
@click.option('prio', '-p', '--prio', '--priority', help='set priority')
@click.option('due', '-d', '--due', '--duedate', '--due-date', help='set due date (uses parsedatetime to parse)')
@click.option('favorite', '-f', '--favorite', '--star', type=click.BOOL, help='mark as favorite')
@click.option('completed', '-c', '--done', '--completed', '--done', type=click.BOOL, help='mark as completed')
@click.option('tag', '-t', '--tag', '--label', help='set tag (tag must exist on server)')
@click.option('reminder', '-r', '--reminder', '--alarm', help='set reminder (uses parsedatetime)')
def task_edit(task_id, **args):
    args_present = {k: v for k, v in args.items() if v is not None}
    if not args_present:
        open_browser(task_id)
    else:
        service.edit_task(task_id, args_present)


@cli.command('ls', help='list tasks')
def task_ls():
    service.list_tasks()


@cli.command('show', help='show task details')
@click.argument('task', required=True, type=click.INT)
def task_show(task):
    service.print_task(task)


@cli.command(name='open', help='open task in browser')
@click.argument('task', required=False, type=click.INT)
def task_open(task):
    open_browser(task)


def open_browser(task):
    url = config.get_parser().get('application', 'frontend_url')
    if task and task > 0:
        url += '/tasks/' + str(task)
    webbrowser.open_new_tab(url)


if __name__ == '__main__':
    cli()
