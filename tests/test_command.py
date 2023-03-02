import datetime
import json
import re

from tests.conftest import invoke
from vja.cli import cli

ADD_SUCCESS_PATTERN = re.compile(r'.*Created task (\d+) in list .*')
TODAY = datetime.datetime.now()
TOMORROW = (datetime.datetime.now() + datetime.timedelta(days=1))
TODAY_ISO = TODAY.isoformat()
TOMORROW_ISO = TOMORROW.isoformat()


class TestAddTask:
    def test_list_id(self, runner):
        res = invoke(runner, 'add title of new task --force --list=1')
        after = json_for_created_task(runner, res.output)
        assert after['tasklist']['id'] == 1

    def test_list_title(self, runner):
        res = invoke(runner, 'add title of new task --force --list=test-list')
        after = json_for_created_task(runner, res.output)
        assert after['tasklist']['title'] == 'test-list'

    def test_duplicate_task_title_rejected(self, runner):
        invoke(runner, 'add title of new task', 1)

    def test_positions_not_null(self, runner):
        res = invoke(runner, 'add any other new task --force')
        after = json_for_created_task(runner, res.output)
        assert after['kanban_position'] > 0
        assert after['position'] > 0

    def test_default_reminder_uses_due(self, runner):
        res = invoke(runner, 'add title of new task --force --list=test-list --due=today --reminder')
        after = json_for_created_task(runner, res.output)
        assert after['due_date'] == after['reminder_dates'][0]

    def test_default_reminder_with_missing_due_uses_tomorrow(self, runner):
        res = invoke(runner, 'add title of new task --force --list=test-list --reminder')
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

        invoke(runner, 'edit 1 --due=today')

        after = json_for_task_id(runner, 1)
        assert datetime.date.today().isoformat()[0:10] in after['due_date']
        assert after['updated'] >= before['updated']

    def test_unset_due_date(self, runner):
        before = json_for_task_id(runner, 1)
        assert before['due_date'] is not None

        invoke(runner, 'edit 1 --due-date=')

        after = json_for_task_id(runner, 1)
        assert after['due_date'] is None
        assert after['updated'] >= before['updated']

    def test_toggle_label(self, runner):
        labels_0 = json_for_task_id(runner, 1)['labels']
        invoke(runner, 'edit 1 --tag=tag1 --force-create')
        labels_1 = json_for_task_id(runner, 1)['labels']
        invoke(runner, 'edit 1 --tag=tag1')
        labels_2 = json_for_task_id(runner, 1)['labels']

        assert labels_0 != labels_1
        assert labels_0 == labels_2
        assert self._has_label_with_title(labels_0, 'tag1') or self._has_label_with_title(labels_1, 'tag1')

    def test_append_note(self, runner):
        invoke(runner, 'edit 1 --note=line1')
        note_1 = json_for_task_id(runner, 1)['description']
        invoke(runner, 'edit 1 --note-append=line2')
        note_2 = json_for_task_id(runner, 1)['description']

        assert note_1 == 'line1'
        assert note_2 == 'line1\nline2'

    def test_edit_list(self, runner):
        invoke(runner, 'list add another list')
        invoke(runner, 'edit 1 --list-id=1')
        list_1 = json_for_task_id(runner, 1)['tasklist']['id']
        invoke(runner, 'edit 1 -l 2')
        list_2 = json_for_task_id(runner, 1)['tasklist']['id']

        assert list_1 == 1
        assert list_2 == 2

    @staticmethod
    def _has_label_with_title(labels, title):
        label_titles = [x['title'] for x in labels]
        return title in label_titles


class TestEditReminder:
    def test_set_default_reminder_to_remote_due(self, runner):
        invoke(runner, f'edit 2 --due-date={TODAY_ISO}')
        invoke(runner, f'edit 2 --reminder={TOMORROW_ISO}')
        before = json_for_task_id(runner, 2)

        invoke(runner, 'edit 2 --reminder')
        after = json_for_task_id(runner, 2)
        assert before['reminder_dates'][0][:10] == TOMORROW.date().isoformat()
        assert after['reminder_dates'][0][:10] == TODAY.date().isoformat()

    def test_set_default_reminder_to_tomorrow(self, runner):
        invoke(runner, 'edit 2 --due-date=')
        invoke(runner, f'edit 2 --reminder={TODAY_ISO}')
        before = json_for_task_id(runner, 2)

        invoke(runner, 'edit 2 --reminder')
        after = json_for_task_id(runner, 2)
        assert before['reminder_dates'][0][:10] == TODAY.date().isoformat()
        assert after['reminder_dates'][0][:10] == TOMORROW.date().isoformat()

    def test_unset_reminder(self, runner):
        invoke(runner, f'edit 2 --reminder={TODAY_ISO}')
        before = json_for_task_id(runner, 2)

        invoke(runner, 'edit 2 --reminder=')
        after = json_for_task_id(runner, 2)
        assert before['reminder_dates'][0][:10] == TODAY.date().isoformat()
        assert not after['reminder_dates']

    def test_set_reminder_to_due(self, runner):
        invoke(runner, f'edit 2 --reminder={TODAY_ISO}')
        before = json_for_task_id(runner, 2)

        invoke(runner, f'edit 2 --due={TOMORROW_ISO} --reminder=due')
        after = json_for_task_id(runner, 2)
        assert before['reminder_dates'][0][:10] == TODAY.date().isoformat()
        assert after['reminder_dates'][0][:10] == TOMORROW.date().isoformat()

    def test_set_reminder_to_value(self, runner):
        invoke(runner, f'edit 2 --reminder={TODAY_ISO}')
        before = json_for_task_id(runner, 2)

        invoke(runner, f'edit 2 --due={TODAY_ISO} --reminder={TOMORROW_ISO}')
        after = json_for_task_id(runner, 2)
        assert before['reminder_dates'][0][:10] == TODAY.date().isoformat()
        assert after['reminder_dates'][0][:10] == TOMORROW.date().isoformat()


    def test_set_reminder_to_value_new_reminder(self, runner):
        invoke(runner, 'edit 2 --reminder=')
        before = json_for_task_id(runner, 2)

        invoke(runner, f'edit 2 --reminder={TOMORROW_ISO}')
        after = json_for_task_id(runner, 2)
        assert not before['reminder_dates']
        assert after['reminder_dates'][0][:10] == TOMORROW.date().isoformat()


class TestToggleDoneTask:
    def test_toggle_done(self, runner):
        done_0 = json_for_task_id(runner, 1)['done']
        invoke(runner, 'check 1')
        done_1 = json_for_task_id(runner, 1)['done']
        invoke(runner, 'check 1')
        done_2 = json_for_task_id(runner, 1)['done']
        assert done_0 != done_1
        assert done_0 == done_2

    def test_toggle_does_not_modify_other_fields(self, runner):
        invoke(runner, 'edit 1 --priority=5')
        json_0 = json_for_task_id(runner, 1)
        invoke(runner, 'check 1')
        json_1 = json_for_task_id(runner, 1)
        invoke(runner, 'check 1')
        json_2 = json_for_task_id(runner, 1)
        assert json_0['priority'] == json_1['priority'] == json_2['priority'] == 5


class TestMultipleTasks:
    def test_edit_three_tasks(self, runner):
        invoke(runner, 'edit 1 2 3 --priority=4')
        for i in range(1, 4):
            after = json_for_task_id(runner, i)
            assert after['priority'] == 4
            assert after['updated'][:10] == TODAY_ISO[:10]
        invoke(runner, 'edit 1 2 3 --priority=5')

    def test_show_three_tasks(self, runner):
        res = invoke(runner, 'show 1 2 3')
        assert res.output.count('\n') >= 30
        assert re.search(r'id: 1', res.output)
        assert re.search(r'id: 2', res.output)
        assert re.search(r'id: 3', res.output)


def json_for_created_task(runner, message):
    assert re.match(ADD_SUCCESS_PATTERN, message), message
    task_id = ADD_SUCCESS_PATTERN.findall(message)[0]
    return json_for_task_id(runner, task_id)


def json_for_task_id(runner, task_id):
    res = invoke(runner, f'show {task_id} --jsonvja')

    assert res.exit_code == 0, res
    data = json.loads(res.output)
    return data
