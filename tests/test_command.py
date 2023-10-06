import datetime
import json
import re

from tests.conftest import invoke

ADD_SUCCESS_PATTERN = re.compile(r'.*Created task (\d+) in project .*')
TODAY = datetime.datetime.now().replace(microsecond=0)
TODAY_ISO = TODAY.isoformat()
YESTERDAY = TODAY + datetime.timedelta(days=-1)
YESTERDAY_ISO = YESTERDAY.isoformat()
TOMORROW = TODAY + datetime.timedelta(days=1)
TOMORROW_ISO = TOMORROW.isoformat()
DATE_1 = TODAY + datetime.timedelta(days=10)
DATE_2 = DATE_1 + datetime.timedelta(days=1)
DATE_1_ISO = DATE_1.isoformat()
DATE_2_ISO = DATE_2.isoformat()


class TestAddTask:
    def test_project_id(self, runner):
        res = invoke(runner, 'add title of new task --force --project=1')
        after = json_for_created_task(runner, res.output)
        assert after['project']['id'] == 1

    def test_project_title(self, runner):
        res = invoke(runner, 'add title of new task --force --project=test-project')
        after = json_for_created_task(runner, res.output)
        assert after['project']['title'] == 'test-project'

    def test_duplicate_task_title_rejected(self, runner):
        invoke(runner, 'add title of new task', 1, catch_exceptions=True)

    def test_default_reminder_uses_due(self, runner):
        res = invoke(runner, 'add title of new task --force --project=test-project --due=today --reminder')
        after = json_for_created_task(runner, res.output)
        assert after['reminders'][0]['relative_period'] == 0
        assert after['reminders'][0]['relative_to'] == 'due_date'

    def test_default_reminder_with_absolute_time(self, runner):
        res = invoke(runner, f'add title of new task --force --project=test-project --reminder={DATE_2_ISO}')
        after = json_for_created_task(runner, res.output)
        assert after['reminders'][0]['reminder'] == DATE_2_ISO


class TestCloneTask:
    def test_clone_task(self, runner):
        invoke(runner, 'pull 1')
        before = json_for_task_id(runner, 1)
        res = invoke(runner, 'clone 1 title of new task cloned from 1')
        after = json_for_created_task(runner, res.output)
        assert after['project'] == before['project']
        assert after['due_date'] == before['due_date']
        assert after['label_objects'] == before['label_objects']
        assert after['title'] != before['title']
        assert after['id'] != before['id']
        assert after['created'] != before['created']
        assert after['position'] != before['position']
        assert after['kanban_position'] != before['kanban_position']
        assert after['bucket_id'] != before['bucket_id']

    def test_clone_task_within_same_bucket(self, runner):
        before = json_for_task_id(runner, 1)
        res = invoke(runner, 'clone 1 --bucket title of new task with labels cloned from 1')
        after = json_for_created_task(runner, res.output)
        assert after['bucket_id'] == before['bucket_id']


class TestEditGeneral:
    def test_edit_title(self, runner):
        before = json_for_task_id(runner, 1)
        new_title = f'{before["title"]}42'
        invoke(runner, ['edit', '1', '-i', f'{new_title}'])

        after = json_for_task_id(runner, 1)
        assert after['title'] == new_title
        assert after['updated'] >= before['updated']
        # other attributes remain in place
        assert after['due_date'] == before['due_date']
        assert after['reminders'] == before['reminders']
        assert after['position'] == before['position']
        assert after['project']['id'] == before['project']['id']
        assert after['created'] == before['created']

    def test_edit_due_date_without_time(self, runner):
        invoke(runner, 'edit 1 --due=tomorrow')

        after = json_for_task_id(runner, 1)
        assert after['due_date'] == (TOMORROW.replace(hour=0, minute=0, second=0)).isoformat()

    def test_edit_due_date_with_time(self, runner):
        invoke(runner, ['edit', '1', '--due=tomorrow 15:00'])

        after = json_for_task_id(runner, 1)
        assert after['due_date'] == (TOMORROW.replace(hour=15, minute=0, second=0)).isoformat()

    def test_unset_due_date(self, runner):
        before = json_for_task_id(runner, 1)
        assert before['due_date'] is not None

        invoke(runner, 'edit 1 --due-date=')

        after = json_for_task_id(runner, 1)
        assert after['due_date'] is None

    def test_toggle_label(self, runner):
        labels_0 = json_for_task_id(runner, 1)['label_objects']
        invoke(runner, 'edit 1 --label=tag1 --force-create')
        labels_1 = json_for_task_id(runner, 1)['label_objects']
        invoke(runner, 'edit 1 --label=tag1')
        labels_2 = json_for_task_id(runner, 1)['label_objects']

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

    def test_edit_project(self, runner):
        invoke(runner, 'project add another project')
        invoke(runner, 'edit 1 --project-id=1')
        project_1 = json_for_task_id(runner, 1)['project']['id']
        invoke(runner, 'edit 1 -o 2')
        project_2 = json_for_task_id(runner, 1)['project']['id']

        assert project_1 == 1
        assert project_2 == 2

    @staticmethod
    def _has_label_with_title(labels, title):
        label_titles = [x['title'] for x in labels]
        return title in label_titles


class TestEditReminder:
    def test_set_reminder_to_absolute_value(self, runner):
        invoke(runner, f'edit 2 --reminder={DATE_1_ISO}')
        before = json_for_task_id(runner, 2)

        invoke(runner, f'edit 2 --due={DATE_1_ISO} --reminder={DATE_2_ISO}')

        after = json_for_task_id(runner, 2)
        assert before['reminders'][0]['reminder'] == DATE_1_ISO
        assert after['reminders'][0]['reminder'] == DATE_2_ISO
        assert not after['reminders'][0]['relative_to']

    def test_set_reminder_to_due(self, runner):
        invoke(runner, f'edit 2 --reminder={DATE_1_ISO}')
        before = json_for_task_id(runner, 2)

        invoke(runner, f'edit 2 --due={DATE_2_ISO} --reminder=due')

        after = json_for_task_id(runner, 2)
        assert before['reminders'][0]['reminder'] == DATE_1_ISO
        assert after['reminders'][0]['reminder'] == DATE_2_ISO
        assert after['reminders'][0]['relative_period'] == 0
        assert after['reminders'][0]['relative_to'] == 'due_date'

    def test_set_reminder_to_due_empty_option(self, runner):
        invoke(runner, f'edit 2 --reminder={DATE_1_ISO}')

        invoke(runner, f'edit 2 --due={DATE_2_ISO} --reminder')

        after = json_for_task_id(runner, 2)
        assert after['reminders'][0]['reminder'] == DATE_2_ISO
        assert after['reminders'][0]['relative_period'] == 0
        assert after['reminders'][0]['relative_to'] == 'due_date'

    def test_set_reminder_to_relative_value(self, runner):
        invoke(runner, f'edit 2 --reminder={DATE_1_ISO}')

        invoke(runner, ['edit', '2', '--due={DATE_2_ISO}', '--reminder=1h1m before due_date'])

        after = json_for_task_id(runner, 2)
        assert after['reminders'][0]['relative_period'] == -3660
        assert after['reminders'][0]['relative_to'] == 'due_date'

    def test_unset_reminder(self, runner):
        invoke(runner, f'edit 2 --reminder={DATE_1_ISO}')
        before = json_for_task_id(runner, 2)

        invoke(runner, 'edit 2 --reminder=')

        after = json_for_task_id(runner, 2)
        assert before['reminders'][0]['reminder'] == DATE_1_ISO
        assert not after['reminders']


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


class TestDeferTask:
    def test_defer_due_date_and_reminder(self, runner):
        invoke(runner, f'edit 2 --due-date={DATE_1_ISO} --reminder={DATE_1_ISO}')

        invoke(runner, 'defer 2 1d')

        after = json_for_task_id(runner, 2)
        assert after['due_date'] == DATE_2_ISO
        assert after['reminders'][0]['reminder'] == DATE_2_ISO

    def test_dont_defer_relative_reminder(self, runner):
        invoke(runner, f'edit 2 --due-date={DATE_1_ISO} -r')

        invoke(runner, 'defer 2 1d')

        after = json_for_task_id(runner, 2)
        assert after['due_date'] == DATE_2_ISO
        assert after['reminders'][0]['relative_period'] == 0
        assert after['reminders'][0]['relative_to'] == 'due_date'

    def test_defer_past_due_realtive_to_now(self, runner):
        invoke(runner, f'edit 2 --due-date={YESTERDAY_ISO}')

        invoke(runner, 'defer 2 1d')

        after = json_for_task_id(runner, 2)
        assert after['due_date'][:10] == TOMORROW_ISO[:10]


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


class TestPushPullTask:
    def test_pull_and_push_back(self, runner):
        bucket_0 = json_for_task_id(runner, 1)['bucket_id']
        invoke(runner, 'pull 1')
        bucket_1 = json_for_task_id(runner, 1)['bucket_id']
        invoke(runner, 'push 1')
        bucket_2 = json_for_task_id(runner, 1)['bucket_id']
        assert bucket_0 != bucket_1
        assert bucket_0 == bucket_2

    def test_repeated_push(self, runner):
        bucket_0 = json_for_task_id(runner, 1)['bucket_id']
        invoke(runner, 'push 1')
        bucket_1 = json_for_task_id(runner, 1)['bucket_id']
        invoke(runner, 'push 1')
        bucket_2 = json_for_task_id(runner, 1)['bucket_id']
        assert bucket_0 == bucket_1
        assert bucket_0 == bucket_2


def json_for_created_task(runner, message):
    assert re.match(ADD_SUCCESS_PATTERN, message), message
    task_id = ADD_SUCCESS_PATTERN.findall(message)[0]
    return json_for_task_id(runner, task_id)


def json_for_task_id(runner, task_id):
    res = invoke(runner, f'show {task_id} --jsonvja')

    assert res.exit_code == 0, res
    data = json.loads(res.output)
    return data
