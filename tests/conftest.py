import os
import subprocess
import sys

import pytest
from click.testing import CliRunner

from vja.cli import cli


@pytest.fixture(name='runner', scope='session')
def setup_runner():
    return CliRunner()


def invoke(runner, command, return_code=0, user_input=None, catch_exceptions=True):
    if isinstance(command, str):
        command = command.split()
    res = runner.invoke(cli, command, input=user_input, catch_exceptions=catch_exceptions)
    assert res.exit_code == return_code, res
    return res


def _login_as_test_user():
    result = subprocess.run('vja logout'.split(), check=False)
    if result.returncode:
        print(result.stdout)
        print(result.stderr)
        return result.returncode

    result = subprocess.run('vja --username=test --password=test user show'.split(), check=False)
    if result.returncode:
        print(result.stdout)
        print(result.stderr)
    return result.returncode


def _create_list_and_task():
    result = subprocess.run('vja list add test-list'.split(), check=False)
    if result.returncode:
        print(result.stdout)
        print(result.stderr)
        return result.returncode
    result = subprocess.run('vja add At least one task --force-create '
                            '--priority=5 --due-date=today --tag=my_tag --favorite=True'.split(), check=False)
    if result.returncode:
        print(result.stdout)
        print(result.stderr)
        return result.returncode
    result = subprocess.run('vja add A task without a label --force-create'.split(), check=False)
    if result.returncode:
        print(result.stdout)
        print(result.stderr)
    return result.returncode


def pytest_configure():
    if 'VJA_CONFIGDIR' not in os.environ:
        print('!!! Precondition not met. You must set VJA_CONFIGDIR in environment variables !!!')
        sys.exit(1)

    if _login_as_test_user() > 0:
        print('!!! Precondition not met. Cannot connect to Vikunja with user test/test')
        sys.exit(1)

    if _create_list_and_task() > 0:
        print('!!! Unable to create default list')
        sys.exit(1)
