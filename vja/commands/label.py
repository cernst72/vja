import click
from click_aliases import ClickAliasedGroup

from vja import VjaError
from vja.cli import with_application, catch_exception


@click.group("label", help="Subcommand: label (see help)", cls=ClickAliasedGroup)
def label_group():
    # vja label
    pass


@label_group.command("ls", help="Print labels ... (id; title)")
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
def label_ls(application, is_json, is_jsonvja, custom_format):
    if custom_format:
        custom_format = application.configuration.get_custom_format_string(
            custom_format
        )
    application.output.label_array(
        application.query_service.find_all_labels(), is_json, is_jsonvja, custom_format
    )


@label_group.command("add", help="Add label with title")
@click.argument("title", required=True, nargs=-1)
@with_application
@catch_exception(handle=VjaError)
def label_add(application, title):
    label = application.command_service.add_label(" ".join(title))
    click.echo(f"Created label {label.id}")
