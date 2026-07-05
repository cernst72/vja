import click
from click_aliases import ClickAliasedGroup

from vja import VjaError
from vja.cli import with_application, catch_exception


@click.group("bucket", help="Subcommand: Kanban buckets (see help)", cls=ClickAliasedGroup)
def bucket_group():
    # vja bucket
    pass


@bucket_group.command(
    "add", help="Add bucket with title to the first Kanban View of the project"
)
@click.option(
    "project", "-o", "--project", "--project-id", help="Create bucket in given project."
)
@click.argument("title", nargs=-1, required=True)
@with_application
@catch_exception(handle=VjaError)
def bucket_add(application, title, project):
    bucket = application.command_service.add_bucket(project, " ".join(title))
    click.echo(f"Created bucket {bucket.id} in project {project}")


@bucket_group.command(
    "ls",
    help="Show Kanban buckets of given project (only the first Kanban View)... "
    "(id; title; limit; count tasks)",
)
@click.option(
    "project_id",
    "-o",
    "--project",
    "--project-id",
    "--project_id",
    required=True,
    type=click.INT,
    help="Show buckets of project with id",
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
def bucket_ls(application, project_id, is_json, is_jsonvja, custom_format):
    if custom_format:
        custom_format = application.configuration.get_custom_format_string(
            custom_format
        )
    application.output.bucket_array(
        application.query_service.find_buckets_in_first_kanban_view(project_id),
        is_json,
        is_jsonvja,
        custom_format,
    )
