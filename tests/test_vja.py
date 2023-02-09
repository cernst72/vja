import logging
import re

import pytest
from click.testing import CliRunner

from vja.cli import cli


@pytest.fixture(name='runner', scope='session')
def setup_runner():
    print("setup_runner---------------------------")
    return CliRunner()


class TestLocalCommands:
    def test_version(self, runner):
        res = runner.invoke(cli, ['--version'])
        assert res.exit_code == 0
        assert re.match(r'.*version \d+\.\d+\.\d+', res.output), res.output

    def test_empty_display_help(self, runner):
        res = runner.invoke(cli)
        assert res.exit_code == 0
        assert 'Usage: cli [OPTIONS] COMMAND [ARGS]...' in res.output
        assert res.output.count('\n') > 20

    def test_help_ls(self, runner):
        res = runner.invoke(cli, ['ls', '--help'])
        assert res.exit_code == 0
        assert 'Usage: cli ls [OPTIONS]' in res.output
        assert 'list tasks' in res.output
        assert res.output.count('\n') > 12


class TestLs:
    def test_help_ls(self, runner, caplog):
        caplog.set_level(logging.DEBUG)
        res = runner.invoke(cli, ['-v', 'ls'], catch_exceptions=True)
        print(caplog.text)
        assert 'Read config from' in caplog.text
        assert 'Connecting to api_url' in caplog.text
        assert res.exit_code == 0, res.output
