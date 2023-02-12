import datetime
import json
import logging
import re

import pytest
from click.testing import CliRunner

from vja.cli import cli

ADD_SUCCESS_PATTERN = re.compile(r'.*Created task (\d+) in list .*')


def execute(runner, command, return_code=0):
    res = runner.invoke(cli, command.split())
    assert res.exit_code == return_code, res
    return res


@pytest.fixture(name='runner', scope='session')
def setup_runner():
    print("setup_runner---------------------------")
    return CliRunner()


class TestBasicOptions:
    def test_version(self, runner):
        res = execute(runner, '--version')
        assert re.match(r'.*version \d+\.\d+\.\d+', res.output), res.output

    def test_no_args_displays_help(self, runner):
        res = execute(runner, '')
        assert 'Usage: cli [OPTIONS] COMMAND [ARGS]...' in res.output
        assert res.output.count('\n') > 20

    def test_help_ls(self, runner):
        res = execute(runner, 'ls --help')
        assert 'Usage: cli ls [OPTIONS]' in res.output
        assert 'list tasks' in res.output
        assert res.output.count('\n') > 12

    def test_verbose_logging(self, runner, caplog):
        caplog.set_level(logging.DEBUG)
        execute(runner, '-v ls')
        print(caplog.text)
        assert 'Read config from' in caplog.text
        assert 'Connecting to api_url' in caplog.text


class TestAddTask:
    def test_list_id(self, runner):
        res = execute(runner, 'add "title of new task" --force --list=1')
        after = json_for_created_task(runner, res.output)
        assert after['tasklist']['id'] == 1

    def test_list_title(self, runner):
        res = execute(runner, 'add "title of new task" --force --list=test-list')
        after = json_for_created_task(runner, res.output)
        assert after['tasklist']['title'] == 'test-list'

    def test_duplicate_task_title_rejected(self, runner):
        res = execute(runner, 'add "title of new task"', 1)
        assert res.exit_code > 0, res

    def test_positions_not_null(self, runner):
        res = execute(runner, 'add "any other new task" --force')
        after = json_for_created_task(runner, res.output)
        assert after['kanban_position'] > 0
        assert after['position'] > 0

    def test_default_reminder_uses_due(self, runner):
        res = execute(runner, 'add "title of new task" --force --list=test-list --due=today --reminder')
        after = json_for_created_task(runner, res.output)
        assert after['due_date'] == after['reminder_dates'][0]

    def test_default_reminder_with_missing_due_uses_tomorrow(self, runner):
        res = execute(runner, 'add "title of new task" --force --list=test-list --reminder')
        after = json_for_created_task(runner, res.output)
        assert after['due_date'] is None
        assert self._tomorrow()[0:10] in after['reminder_dates'][0]

    @staticmethod
    def _tomorrow():
        return (datetime.date.today() + datetime.timedelta(days=1)).isoformat()


class TestEditTask:
    def test_edit_title(self, runner):
        before = json_for_task_id(runner, 1)
        new_title = f'{before["title"]}42'
        # execute(runner, f'edit 1 -i "new')
        res = runner.invoke(cli, ['edit', '1', '-i', f'{new_title}'])
        assert res.exit_code == 0, res

        after = json_for_task_id(runner, 1)
        assert after['title'] == new_title
        # other attributes remain in place
        assert after['due_date'] == before['due_date']
        assert after['position'] == before['position']
        assert after['tasklist']['id'] == before['tasklist']['id']
        assert after['created'] == before['created']
        assert after['updated'] >= before['updated']

    def test_edit_due_date(self, runner):
        before = json_for_task_id(runner, 1)

        execute(runner, 'edit 1 --due=today')

        after = json_for_task_id(runner, 1)
        assert datetime.date.today().isoformat()[0:10] in after['due_date']
        assert after['updated'] >= before['updated']

    def test_unset_due_date(self, runner):
        before = json_for_task_id(runner, 1)
        assert before['due_date'] is not None

        execute(runner, 'edit 1 --due-date=')

        after = json_for_task_id(runner, 1)
        assert after['due_date'] is None
        assert after['updated'] >= before['updated']

    def test_toggle_label(self, runner):
        tags_0 = json_for_task_id(runner, 1)['labels']
        execute(runner, 'edit 1 --tag=tag1 --force-create')
        tags_1 = json_for_task_id(runner, 1)['labels']
        execute(runner, 'edit 1 --tag=tag1')
        tags_2 = json_for_task_id(runner, 1)['labels']

        assert tags_0 != tags_1
        assert tags_0 == tags_2
        assert self._has_label_with_title(tags_0, 'tag1') or self._has_label_with_title(tags_1, 'tag1')

    @staticmethod
    def _has_label_with_title(labels, title):
        label_titles = [x['title'] for x in labels]
        return title in label_titles


# set reminder to due-date of task
# unset reminder
# set reminder to new value
# set reminder to given due-date
# add label
# remove label

def json_for_created_task(runner, message):
    assert re.match(ADD_SUCCESS_PATTERN, message), message
    task_id = ADD_SUCCESS_PATTERN.findall(message)[0]
    return json_for_task_id(runner, task_id)


def json_for_task_id(runner, task_id):
    res = execute(runner, f'show {task_id} --jsonvja')

    assert res.exit_code == 0, res
    data = json.loads(res.output)
    return data
