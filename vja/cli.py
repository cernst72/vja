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
@click.option('-v', '--verbose', default=False, is_flag=True, help='verbose output')
@click.option('-u', '--username', 'username', help='username for initial login (optional)')
@click.option('-p', '--password', 'password', help='password for initial login (optional)')
def cli(verbose, username=None, password=None):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
        logger.setLevel(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
        logger.setLevel(level=logging.INFO)
    if username or password:
        service.authenticate(username, password)


@cli.command("help")
@click.argument('subcommand')
@click.pass_context
def help_command(ctx, subcommand):
    subcommand_obj = cli.get_command(ctx, subcommand)
    if subcommand_obj is None:
        click.echo("I don't know that command.")
    else:
        click.echo(subcommand_obj.get_help(ctx))


# namespaces
@cli.group("namespace", help="subcommand: namespace (see help)")
def namespace_group():
    pass


@namespace_group.command("ls", help="print namespaces")
def namespace_ls():
    service.print_namespaces()


# lists
@cli.group("list", help="subcommand: list (see help)")
def list_group():
    pass


@list_group.command("add", help="add list with title")
@click.option('namespace_id', '-n', '--namespace-id', help='create list in namespace, default: first list found')
@click.argument('title', nargs=-1)
def list_add(title, namespace_id=None):
    service.add_list(namespace_id, " ".join(title))


@list_group.command("ls", help="print lists")
def list_ls():
    service.print_lists()


# labels
@cli.group("label", help="subcommand: label (see help)")
def label_group():
    pass


@label_group.command("ls", help="print labels")
def label_ls():
    service.print_labels()


# tasks
@cli.command('add', help='add new task')
@click.argument('line', nargs=-1)
@click.option('list_id', '-l', '--list-id', type=click.INT, help='create task in list, default: first namespace found')
def task_add(line, list_id=None):
    service.add_task(list_id, " ".join(line))


@cli.command('ls', help='list tasks')
def task_ls():
    service.list_tasks()


@cli.command('report', help='list relevant tasks (optionaly with -a)')
@click.option('-l', '--list', 'list_name', help='filter by list')
@click.option('-a', '--all', 'all_size', count=True, help='show additional tasks (tomorrow + task without due date)')
@click.option('-i', '--urgency', 'urgency_sort', is_flag=True, help='sort by priority level')
def task_report(list_name=None, all_size=0, urgency_sort=False):
    service.report_tasks(list_name, all_size, urgency_sort)


@cli.command('show', help='show task details')
@click.argument('task', required=True, type=click.INT)
def task_show(task):
    service.print_task(task)


@cli.command(name='open', help='open task in browser')
@click.argument('task', required=False, type=click.INT)
def task_open(task):
    # TODO restore cache logic
    url = config.get_parser().get('application', 'frontend_url')
    if task and task > 0:
        url += "/tasks/" + str(task)
    webbrowser.open_new_tab(url)


@cli.command('edit', help='modify task')
@click.argument('task', required=True, type=click.INT)
@click.argument('line', nargs=-1)
# @click.argument('modification', required=True, type=click.STRING)
def task_edit(task, line):
    return


@cli.command('complete', help='mark task as complete')
@click.argument('task', required=True, type=click.INT)
def task_complete(task):
    return


if __name__ == '__main__':
    cli()
