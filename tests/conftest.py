import logging
import os
import subprocess
import sys

import pytest
from click.testing import CliRunner

from vja.cli import cli

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


@pytest.fixture(name='runner', scope='session')
def setup_runner():
    return CliRunner()


def invoke(runner, command, return_code=0, user_input=None, catch_exceptions=False):
    if isinstance(command, str):
        command = command.split()
    res = runner.invoke(cli, command, input=user_input, catch_exceptions=catch_exceptions)
    sys.stdout.write(res.output)
    if res.stderr_bytes:
        sys.stdout.write(res.stderr_bytes)
    if res.exception:
        logging.warning(res.exception)
    assert res.exit_code == return_code, res
    return res


def _login_as_test_user():
    run_vja('vja logout')
    run_vja('vja --username=test --password=test user show')


def _create_project_and_task():
    run_vja('vja project add test-project')
    run_vja('vja project add child --parent-project=test-project')
    run_vja('vja project add grand-child --parent-project=child')
    run_vja('vja bucket add --project=test-project Second bucket')
    run_vja('vja add At least one task --force-create --priority=5 --due-date=today --label=my_tag --favorite=True --project-id=test-project')
    run_vja('vja add Task in subproject --force-create --project-id=grand-child')
    run_vja('vja add A task without a label --force-create')


def run_vja(command):
    result = subprocess.run(command.split(), capture_output=True, check=False)
    if result.returncode:
        print(f'!!! Non-zero result ({result.returncode}) from command {command}')
        sys.stdout.write(result.stdout.decode('utf-8'))
        sys.stdout.write(result.stderr.decode('utf-8'))
        sys.exit(1)


def pytest_configure():
    if 'VJA_CONFIGDIR' not in os.environ:
        print('!!! Precondition not met. You must set VJA_CONFIGDIR in environment variables !!!')
        sys.exit(1)

    _login_as_test_user()

    _create_project_and_task()
