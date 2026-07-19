import click
from click_aliases import ClickAliasedGroup

from vja import VjaError
from vja.application import Application, catch_exception, with_application


@click.group("project", help="Subcommand: project (see help)", cls=ClickAliasedGroup)
def project_group():
    # vja project
    pass


@project_group.command("add", help="Add project with title")
@click.option(
    "parent_project",
    "-o",
    "--parent-project",
    "--parent_project",
    help="Create project as child of parent project. May be given by id or title of parent-project.",
)
@click.argument("title", nargs=-1, required=True)
@with_application
@catch_exception(handle=VjaError)
def project_add(application: Application, title, parent_project=None):
    project = application.command_service.add_project(parent_project, " ".join(title))
    click.echo(f"Created project {project.id}")


@project_group.command(
    "ls",
    aliases=["list"],
    help="Print projects ... (id; title; description; parent_project_id)",
)
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
@with_application
@catch_exception(handle=VjaError)
def project_ls(application: Application, is_json, is_jsonvja, custom_format):
    if custom_format:
        custom_format = application.configuration.get_custom_format_string(
            custom_format
        )
    application.output.project_array(
        application.query_service.find_all_projects(),
        is_json,
        is_jsonvja,
        custom_format,
    )


@project_group.command("show", help="Show project details")
@click.argument("project_id", required=True, type=click.INT)
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
def project_show(application: Application, project_id, is_json, is_jsonvja):
    application.output.project(
        application.query_service.find_project_by_id(project_id), is_json, is_jsonvja
    )


@project_group.command("open", help="Open project in webbrowser")
@click.argument("project_id", required=True, type=click.INT)
@with_application
@catch_exception(handle=VjaError)
def project_open(application: Application, project_id):
    application.open_browser_project(project_id)
