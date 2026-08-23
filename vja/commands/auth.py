import click

from vja import VjaError
from vja.application import Application, catch_exception, with_application


@click.command("logout", help="Remove local access token")
@with_application
@catch_exception(handle=VjaError)
def logout(application: Application) -> None:
    application.command_service.logout()
