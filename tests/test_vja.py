import datetime
import json
import logging
import re

import pytest
from click.testing import CliRunner

from vja.cli import cli
from vja.config import VjaConfiguration

ADD_SUCCESS_PATTERN = re.compile(r'.*Created task (\d+) in list .*')
TODAY = datetime.datetime.now()
TOMORROW = (datetime.datetime.now() + datetime.timedelta(days=1))
TODAY_ISO = TODAY.isoformat()
TOMORROW_ISO = TOMORROW.isoformat()


def execute(runner, command, return_code=0, user_input=None, catch_exceptions=True):
    res = runner.invoke(cli, command.split(), input=user_input, catch_exceptions=catch_exceptions)
    assert res.exit_code == return_code, res
    return res


@pytest.fixture(name='runner', scope='session')
def setup_runner():
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
        assert 'Read config from' in caplog.text
        assert 'Connecting to api_url' in caplog.text


class TestAddTask:
    def test_list_id(self, runner):
        res = execute(runner, 'add title of new task --force --list=1')
        after = json_for_created_task(runner, res.output)
        assert after['tasklist']['id'] == 1

    def test_list_title(self, runner):
        res = execute(runner, 'add title of new task --force --list=test-list')
        after = json_for_created_task(runner, res.output)
        assert after['tasklist']['title'] == 'test-list'

    def test_duplicate_task_title_rejected(self, runner):
        execute(runner, 'add title of new task', 1)

    def test_positions_not_null(self, runner):
        res = execute(runner, 'add any other new task --force')
        after = json_for_created_task(runner, res.output)
        assert after['kanban_position'] > 0
        assert after['position'] > 0

    def test_default_reminder_uses_due(self, runner):
        res = execute(runner, 'add title of new task --force --list=test-list --due=today --reminder')
        after = json_for_created_task(runner, res.output)
        assert after['due_date'] == after['reminder_dates'][0]

    def test_default_reminder_with_missing_due_uses_tomorrow(self, runner):
        res = execute(runner, 'add title of new task --force --list=test-list --reminder')
        after = json_for_created_task(runner, res.output)
        assert after['due_date'] is None
        assert TOMORROW_ISO[0:10] in after['reminder_dates'][0]


class TestEditGeneral:
    def test_edit_title(self, runner):
        before = json_for_task_id(runner, 1)
        new_title = f'{before["title"]}42'
        res = runner.invoke(cli, ['edit', '1', '-i', f'{new_title}'])
        assert res.exit_code == 0, res

        after = json_for_task_id(runner, 1)
        assert after['title'] == new_title
        assert after['updated'] > before['updated']
        # other attributes remain in place
        assert after['due_date'] == before['due_date']
        assert after['reminder_dates'] == before['reminder_dates']
        assert after['position'] == before['position']
        assert after['tasklist']['id'] == before['tasklist']['id']
        assert after['created'] == before['created']

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
        labels_0 = json_for_task_id(runner, 1)['labels']
        execute(runner, 'edit 1 --tag=tag1 --force-create')
        labels_1 = json_for_task_id(runner, 1)['labels']
        execute(runner, 'edit 1 --tag=tag1')
        labels_2 = json_for_task_id(runner, 1)['labels']

        assert labels_0 != labels_1
        assert labels_0 == labels_2
        assert self._has_label_with_title(labels_0, 'tag1') or self._has_label_with_title(labels_1, 'tag1')

    def test_append_note(self, runner):
        execute(runner, 'edit 1 --note=line1')
        note_1 = json_for_task_id(runner, 1)['description']
        execute(runner, 'edit 1 --note-append=line2')
        note_2 = json_for_task_id(runner, 1)['description']

        assert note_1 == 'line1'
        assert note_2 == 'line1\nline2'

    @staticmethod
    def _has_label_with_title(labels, title):
        label_titles = [x['title'] for x in labels]
        return title in label_titles


class TestEditReminder:
    def test_set_reminder_to_task(self, runner):
        execute(runner, f'edit 2 --due-date={TOMORROW_ISO}')
        execute(runner, f'edit 2 --reminder={TODAY_ISO}')
        before = json_for_task_id(runner, 2)

        execute(runner, 'edit 2 --reminder')
        after = json_for_task_id(runner, 2)
        assert before['reminder_dates'][0][:10] == TODAY.date().isoformat()
        assert after['reminder_dates'][0][:10] == TOMORROW.date().isoformat()

    def test_unset_reminder(self, runner):
        execute(runner, f'edit 2 --reminder={TODAY_ISO}')
        before = json_for_task_id(runner, 2)

        execute(runner, 'edit 2 --reminder=')
        after = json_for_task_id(runner, 2)
        assert before['reminder_dates'][0][:10] == TODAY.date().isoformat()
        assert after['reminder_dates'][0] is None

    def test_set_reminder_to_due(self, runner):
        execute(runner, f'edit 2 --reminder={TODAY_ISO}')
        before = json_for_task_id(runner, 2)

        execute(runner, f'edit 2 --due={TOMORROW_ISO} --reminder=due')
        after = json_for_task_id(runner, 2)
        assert before['reminder_dates'][0][:10] == TODAY.date().isoformat()
        assert after['reminder_dates'][0][:10] == TOMORROW.date().isoformat()


class TestToggleDoneTask:
    def test_toggle_done(self, runner):
        done_0 = json_for_task_id(runner, 1)['done']
        execute(runner, 'check 1')
        done_1 = json_for_task_id(runner, 1)['done']
        execute(runner, 'check 1')
        done_2 = json_for_task_id(runner, 1)['done']
        assert done_0 != done_1
        assert done_0 == done_2

    def test_toggle_does_not_modify_other_fields(self, runner):
        execute(runner, 'edit 1 --priority=5')
        json_0 = json_for_task_id(runner, 1)
        execute(runner, 'check 1')
        json_1 = json_for_task_id(runner, 1)
        execute(runner, 'check 1')
        json_2 = json_for_task_id(runner, 1)
        assert json_0['priority'] == json_1['priority'] == json_2['priority'] == 5


class TestMultipleTasks:
    def test_edit_three_tasks(self, runner):
        execute(runner, 'edit 1 2 3 --priority=4')
        for i in range(1, 4):
            after = json_for_task_id(runner, i)
            assert after['priority'] == 4
            assert after['updated'][:10] == TODAY_ISO[:10]

    def test_show_three_tasks(self, runner):
        res = execute(runner, 'show 1 2 3')
        assert res.output.count('\n') >= 30


class TestLoginLogout:
    def test_logout_login_given_password(self, runner, caplog):
        execute(runner, 'logout')
        assert 'Logged out' in caplog.text
        execute(runner, '-u test -p test user show')

    def test_logout_login_wrong_given_password(self, runner, caplog):
        execute(runner, 'logout')
        assert 'Logged out' in caplog.text
        with pytest.raises(Exception) as exception:
            execute(runner, '-u testxx -p testxx user show', return_code=1)
            assert '412 Client Error' in exception.value
        execute(runner, '-u test -p test user show')

    def test_logout_login_password_from_stdin(self, runner, caplog):
        execute(runner, 'logout')
        assert 'Logged out' in caplog.text
        execute(runner, 'user show', user_input='test\ntest\n')
        assert 'Login successful' in caplog.text

    def test_logout_login_wrong_password_from_stdin(self, runner, caplog):
        execute(runner, 'logout')
        assert 'Logged out' in caplog.text
        with pytest.raises(Exception) as exception:
            execute(runner, 'user show', user_input='testy\ntesty\n')
            assert '412 Client Error' in exception.value
        execute(runner, '-u test -p test user show')

    def test_prompt_when_invalid_token(self, runner, caplog):
        self._invalidate_token()
        execute(runner, 'user show', user_input='test\ntest\n')
        assert 'trying to retrieve new access token' in caplog.text
        assert 'Login successful' in caplog.text

    def test_http_error(self, runner, caplog):
        execute(runner, 'show 9999', return_code=1)
        assert 'HTTP-Error 404' in caplog.text

    @staticmethod
    def _invalidate_token():
        config = VjaConfiguration()
        with open(config.get_token_file(), 'w', encoding='utf-8') as token_file:
            json.dump({'token': 'slightly outdated...'}, token_file)


def json_for_created_task(runner, message):
    assert re.match(ADD_SUCCESS_PATTERN, message), message
    task_id = ADD_SUCCESS_PATTERN.findall(message)[0]
    return json_for_task_id(runner, task_id)


def json_for_task_id(runner, task_id):
    res = execute(runner, f'show {task_id} --jsonvja')

    assert res.exit_code == 0, res
    data = json.loads(res.output)
    return data
