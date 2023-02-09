import datetime
import json
import logging
import re

import pytest
from click.testing import CliRunner

from vja.cli import cli

ADD_SUCCESS_PATTERN = re.compile(r'.*Created task (\d+) in list .*')


@pytest.fixture(name='runner', scope='session')
def setup_runner():
    print("setup_runner---------------------------")
    return CliRunner()


class TestBasicOptions:
    def test_version(self, runner):
        res = runner.invoke(cli, ['--version'])
        assert res.exit_code == 0, res
        assert re.match(r'.*version \d+\.\d+\.\d+', res.output), res.output

    def test_no_args_displays_help(self, runner):
        res = runner.invoke(cli)
        assert res.exit_code == 0, res
        assert 'Usage: cli [OPTIONS] COMMAND [ARGS]...' in res.output
        assert res.output.count('\n') > 20

    def test_help_ls(self, runner):
        res = runner.invoke(cli, ['ls', '--help'])
        assert res.exit_code == 0, res
        assert 'Usage: cli ls [OPTIONS]' in res.output
        assert 'list tasks' in res.output
        assert res.output.count('\n') > 12

    def test_verbose_logging(self, runner, caplog):
        caplog.set_level(logging.DEBUG)
        res = runner.invoke(cli, ['-v', 'ls'], catch_exceptions=True)
        assert res.exit_code == 0, res
        print(caplog.text)
        assert 'Read config from' in caplog.text
        assert 'Connecting to api_url' in caplog.text


class TestAddTask:
    def test_list_id(self, runner):
        res = runner.invoke(cli, 'add "title of new task" --force --list=1'.split())
        assert res.exit_code == 0, res
        data = json_for_created_task(runner, res.output)
        assert data['tasklist']['id'] == 1

    def test_list_title(self, runner):
        res = runner.invoke(cli, 'add "title of new task" --force --list=test-list'.split())
        assert res.exit_code == 0, res
        data = json_for_created_task(runner, res.output)
        assert data['tasklist']['title'] == 'test-list'

    def test_duplicate_task_title_rejected(self, runner):
        res = runner.invoke(cli, 'add "title of new task"'.split())
        assert res.exit_code > 0, res

    def test_positions_not_null(self, runner):
        res = runner.invoke(cli, 'add "any other new task" --force'.split())
        assert res.exit_code == 0, res
        data = json_for_created_task(runner, res.output)
        assert data['kanban_position'] > 0
        assert data['position'] > 0

    def test_default_reminder_uses_due(self, runner):
        res = runner.invoke(cli, 'add "title of new task" --force --list=test-list --due=today --reminder'.split())
        assert res.exit_code == 0, res
        data = json_for_created_task(runner, res.output)
        assert data['due_date'] == data['reminder_dates'][0]

    def test_default_reminder_with_missing_due_uses_tomorrow(self, runner):
        res = runner.invoke(cli, 'add "title of new task" --force --list=test-list --reminder'.split())
        assert res.exit_code == 0, res
        data = json_for_created_task(runner, res.output)
        assert data['due_date'] is None
        assert self.tomorrow()[0:10] in data['reminder_dates'][0]

    def tomorrow(self):
        return (datetime.date.today() + datetime.timedelta(days=1)).isoformat()


def json_for_created_task(runner, message):
    assert re.match(ADD_SUCCESS_PATTERN, message), message
    task_id = ADD_SUCCESS_PATTERN.findall(message)[0]
    res = runner.invoke(cli, ['show', '--jsonvja', task_id])
    assert res.exit_code == 0, res
    data = json.loads(res.output)
    return data
