import logging
import os
import subprocess
import sys

import pytest
from click.testing import CliRunner

from vja.cli import cli

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


@pytest.fixture(name="runner", scope="session")
def setup_runner():
    return CliRunner()


# Evaluate pytest options
def pytest_addoption(parser):
    parser.addoption("--oldapi", action="store_true")


@pytest.fixture
def use_old_api(request):
    return request.config.getoption("oldapi") or False

def invoke(runner, command, use_old_api=False, return_code=0, user_input=None, catch_exceptions=False):
    if isinstance(command, str):
        command = command.split()
    if use_old_api:
        command = ["--oldapi"] + command
    res = runner.invoke(
        cli, command, input=user_input, catch_exceptions=catch_exceptions
    )
    sys.stdout.write(res.output)
    if res.stderr_bytes:
        sys.stdout.write(res.stderr)
    if res.exception:
        logging.warning(res.exception)
    if return_code:
        assert res.exit_code == return_code, res
    return res


def _login_as_test_user():
    run_vja("logout")
    run_vja("--username=test --password=test user show")


def _create_project_and_task(use_old_api):
    run_vja("project add test-project")
    run_vja("project add child --parent-project=test-project")
    run_vja("project add grand-child --parent-project=child")
    run_vja("bucket add --project=test-project Second bucket")
    run_vja(
        "task add At least one task --force-create --priority=5 --due-date=today --label=my_tag --favorite --project-id=test-project"
    )
    run_vja("task add Task in subproject --force-create --project-id=grand-child")
    run_vja("task add A task without a label --force-create")
    run_vja("task ls", use_old_api)
    run_vja("task show 1")


def run_vja(command, use_old_api=False):
    vja_command = "vja " + ("--oldapi " if use_old_api else "") + command
    result = subprocess.run(vja_command.split(), capture_output=True, check=False)
    if result.returncode:
        print(f"!!! Non-zero result ({result.returncode}) from command {command}")
        sys.stdout.write(result.stdout.decode("utf-8"))
        sys.stdout.write(result.stderr.decode("utf-8"))
        sys.exit(1)


def pytest_configure(config):
    use_old_api = config.getoption("oldapi") or False
    if "VJA_CONFIGDIR" not in os.environ:
        print(
            "!!! Precondition not met. You must set VJA_CONFIGDIR in environment variables !!!"
        )
        sys.exit(1)

    _login_as_test_user()

    _create_project_and_task(use_old_api)
