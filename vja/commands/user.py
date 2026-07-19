import click

from vja import VjaError
from vja.application import Application, catch_exception, with_application


@click.group("user", help="Subcommand: user (see help)")
def user_group():
    # vja user
    pass


@user_group.command("show", help="Print current user")
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
def user_show(application: Application, is_json=False, is_jsonvja=False):
    application.output.user(
        application.query_service.find_current_user(), is_json, is_jsonvja
    )
