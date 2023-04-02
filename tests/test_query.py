import json
import re

from tests.conftest import invoke


class TestUser:
    def test_user_show(self, runner):
        res = invoke(runner, 'user show')
        assert re.search(r'username=\'test\'', res.output)

    def test_user_show_json(self, runner):
        res = invoke(runner, 'user show --json')
        assert json.loads(res.output)['username'] == 'test'

    def test_user_show_jsonvja(self, runner):
        res = invoke(runner, 'user show --jsonvja')
        assert json.loads(res.output)['username'] == 'test'


class TestProject:
    def test_project_ls(self, runner):
        res = invoke(runner, 'project ls')
        assert re.search(r'test-project', res.output)

    def test_project_show(self, runner):
        res = invoke(runner, 'project show 1')
        assert len(res.output) > 0

    def test_project_ls_custom_format(self, runner):
        res = invoke(runner, 'project ls --custom-format=ids_only')
        for line in res.output:
            assert re.match(r'^\d*$', line)


class TestBucket:
    def test_bucket_ls(self, runner):
        res = invoke(runner, 'bucket ls --project-id=1')
        assert re.search(r'Backlog', res.output)

    def test_bucket_ls_custom_format(self, runner):
        res = invoke(runner, 'bucket ls --project-id=1 --custom-format=ids_only')
        for line in res.output:
            assert re.match(r'^\d*$', line)


class TestLabel:
    def test_label_ls(self, runner):
        res = invoke(runner, 'label ls')
        assert re.search(r'my_tag', res.output)

    def test_label_ls_custom_format(self, runner):
        res = invoke(runner, 'label ls --custom-format=ids_only')
        for line in res.output:
            assert re.match(r'^\d*$', line)


class TestSingleTask:
    def test_task_show(self, runner):
        res = invoke(runner, 'show 1')
        assert re.search(r'id: 1', res.output)

    def test_task_show_json(self, runner):
        res = invoke(runner, 'show 1 --json')
        assert json.loads(res.output)['id'] == 1

    def test_task_show_jsonvja(self, runner):
        res = invoke(runner, 'show 1 --jsonvja')
        data = json.loads(res.output)
        assert data['id'] == 1
        assert data['title'] is not None
        assert data['position'] is not None
        assert data['kanban_position'] is not None
        assert data['bucket_id'] is not None
        assert data['project']['id'] is not None
        assert data['created'] is not None
        assert data['updated'] is not None


class TestTaskLs:
    def test_task_ls(self, runner):
        res = invoke(runner, 'ls')
        assert re.search(r'At least one task', res.output)

    def test_task_ls_json(self, runner):
        res = invoke(runner, 'ls --json')
        assert json.loads(res.output)[0]['title'] is not None

    def test_task_ls_jsonvja(self, runner):
        res = invoke(runner, 'ls --jsonvja')
        data = json.loads(res.output)[0]
        assert data['title'] is not None

    def test_sort_id(self, runner):
        res = invoke(runner, ['ls', '--jsonvja', '--sort=id'])
        data = json.loads(res.output)
        assert data[0]['id'] == 1
        res = invoke(runner, ['ls', '--jsonvja', '--sort=-id'])
        data = json.loads(res.output)
        assert data[0]['id'] > 1

    def test_sort_combined(self, runner):
        res = invoke(runner, ['ls', '--jsonvja', '--sort=due_date, is_favorite, -priority, project.title'])
        data = json.loads(res.output)
        assert data[0]['due_date'] is not None
        assert data[-1]['due_date'] is None

    def test_task_custom_format(self, runner):
        res = invoke(runner, 'ls --custom-format=ids_only')
        for line in res.output:
            assert re.match(r'^\d*$', line)


class TestTaskLsFilter:
    def test_task_filter_bucket(self, runner):
        res = invoke(runner, ['ls', '--jsonvja', '--bucket=1'])
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(i['bucket_id'] == 1 for i in data)
        res = invoke(runner, ['ls', '--jsonvja', '--bucket=9999'])
        data = json.loads(res.output)
        assert len(data) == 0

    def test_task_filter_due(self, runner):
        res = invoke(runner, ['ls', '--jsonvja', '--due-date=after yesterday'])
        data = json.loads(res.output)
        assert len(data) > 0
        res = invoke(runner, ['ls', '--jsonvja', '--due-date=before tomorrow'])
        data = json.loads(res.output)
        assert len(data) > 0
        res = invoke(runner, ['ls', '--jsonvja', '--due-date=after next week'])
        data = json.loads(res.output)
        assert len(data) == 0
        res = invoke(runner, ['ls', '--jsonvja', '--due-date='''''''])
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(i['due_date'] is None for i in data)

    def test_task_filter_favorite(self, runner):
        res = invoke(runner, ['ls', '--jsonvja', '--favorite=True'])
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(i['is_favorite'] for i in data)

    def test_task_filter_label(self, runner):
        res = invoke(runner, ['ls', '--jsonvja', '--label=my_tag'])
        data = json.loads(res.output)
        assert len(data) > 0
        assert data[0]['labels'][0]['title'] == 'my_tag'
        res = invoke(runner, ['ls', '--jsonvja', '--label=Not created'])
        data = json.loads(res.output)
        assert len(data) == 0

    def test_task_filter_label_empty(self, runner):
        res = invoke(runner, ['ls', '--jsonvja', '--label='''''''])
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(len(i['labels']) == 0 for i in data)

    def test_task_filter_project(self, runner):
        res = invoke(runner, ['ls', '--jsonvja', '--project=test-project'])
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(i['project']['title'] == 'test-project' for i in data)
        res = invoke(runner, ['ls', '--jsonvja', '--project=Not created'])
        data = json.loads(res.output)
        assert len(data) == 0

    def test_task_filter_priority(self, runner):
        res = invoke(runner, ['ls', '--jsonvja', '--priority=eq 5'])
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(i['priority'] == 5 for i in data)
        res = invoke(runner, ['ls', '--jsonvja', '--priority=gt 4'])
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(i['priority'] > 4 for i in data)
        res = invoke(runner, ['ls', '--jsonvja', '--priority=gt 5'])
        data = json.loads(res.output)
        assert len(data) == 0

    def test_task_filter_title(self, runner):
        res = invoke(runner, ['ls', '--jsonvja', '--title=At least one'])
        data = json.loads(res.output)
        assert len(data) > 0
        assert all('At least one task' in i['title'] for i in data)
        res = invoke(runner, ['ls', '--jsonvja', '--title=Not created'])
        data = json.loads(res.output)
        assert len(data) == 0

    def test_task_filter_urgency(self, runner):
        res = invoke(runner, ['ls', '--jsonvja', '--urgency=10'])
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(i['urgency'] >= 10 for i in data)
        res = invoke(runner, ['ls', '--jsonvja', '--urgency=10000'])
        data = json.loads(res.output)
        assert len(data) == 0

    def test_task_filter_general(self, runner):
        res = invoke(runner, ['ls', '--jsonvja', '--filter=title contains At least one'])
        assert len(json.loads(res.output)) > 0
        res = invoke(runner, ['ls', '--jsonvja', '--filter=title contains TASK_NOT_CREATED'])
        assert len(json.loads(res.output)) == 0
        res = invoke(runner, ['ls', '--jsonvja', '--filter=priority gt 2'])
        assert len(json.loads(res.output)) > 0
        res = invoke(runner, ['ls', '--jsonvja', '--filter=priority gt 5'])
        assert len(json.loads(res.output)) == 0
        res = invoke(runner, ['ls', '--jsonvja', '--filter=due_date after 2 days ago'])
        assert len(json.loads(res.output)) > 0
        res = invoke(runner, ['ls', '--jsonvja', '--filter=due_date after 200 days'])
        assert len(json.loads(res.output)) == 0
        res = invoke(runner, ['ls', '--jsonvja', '--filter=due_date after 200 days'])
        assert len(json.loads(res.output)) == 0
        res = invoke(runner, ['ls', '--jsonvja', '--filter=is_favorite eq True'])
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(i['is_favorite'] for i in data)

    def test_task_filter_general_combined(self, runner):
        res = invoke(runner, ['ls', '--jsonvja', '--filter=id gt 0', '--filter=id lt 2'])
        data = json.loads(res.output)
        assert len(data) == 1
        assert all(i['id'] == 1 for i in data)
