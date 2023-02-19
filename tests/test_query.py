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


class TestNamespace:
    def test_namespace_ls(self, runner):
        res = invoke(runner, 'namespace ls')
        assert re.search(r'test\'s namespace', res.output)

    def test_namespace_ls_json(self, runner):
        res = invoke(runner, 'namespace ls --json')
        assert json.loads(res.output)[1]['title'] == 'test'

    def test_namespace_ls_jsonvja(self, runner):
        res = invoke(runner, 'namespace ls --jsonvja')
        assert json.loads(res.output)[1]['title'] == 'test'

    def test_namespace_ls_custom_format(self, runner):
        res = invoke(runner, 'namespace ls --custom-format=ids_only')
        for line in res.output:
            assert re.match(r'^-?\d*$', line)


class TestList:
    def test_list_ls(self, runner):
        res = invoke(runner, 'list ls')
        assert re.search(r'test-list', res.output)

    def test_list_show(self, runner):
        res = invoke(runner, 'list show 1')
        assert len(res.output) > 0

    def test_list_ls_custom_format(self, runner):
        res = invoke(runner, 'list ls --custom-format=ids_only')
        for line in res.output:
            assert re.match(r'^\d*$', line)


class TestBucket:
    def test_bucket_ls(self, runner):
        res = invoke(runner, 'bucket ls --list-id=1')
        assert re.search(r'Backlog', res.output)

    def test_bucket_ls_custom_format(self, runner):
        res = invoke(runner, 'bucket ls --list-id=1 --custom-format=ids_only')
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
        assert data['tasklist']['id'] is not None
        assert data['created'] is not None
        assert data['updated'] is not None


class TestTaskList:
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

    def test_task_filter_favorite(self, runner):
        res = invoke(runner, ['ls', '--jsonvja', '--favorite=True'])
        data = json.loads(res.output)
        assert len(data) > 0
        assert data[0]['is_favorite']

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

    def test_task_filter_list(self, runner):
        res = invoke(runner, ['ls', '--jsonvja', '--list=test-list'])
        data = json.loads(res.output)
        assert len(data) > 0
        assert data[0]['tasklist']['title'] == 'test-list'
        res = invoke(runner, ['ls', '--jsonvja', '--list=Not created'])
        data = json.loads(res.output)
        assert len(data) == 0

    def test_task_filter_namespace(self, runner):
        res = invoke(runner, ['ls', '--jsonvja', '--namespace=test'])
        data = json.loads(res.output)
        assert len(data) > 0
        assert data[0]['tasklist']['namespace']['title'] == 'test'
        res = invoke(runner, ['ls', '--jsonvja', '--namespace=Not created'])
        data = json.loads(res.output)
        assert len(data) == 0

    def test_task_filter_title(self, runner):
        res = invoke(runner, ['ls', '--jsonvja', '--title=At least one'])
        data = json.loads(res.output)
        assert len(data) > 0
        assert data[0]['title'] == 'At least one task'
        res = invoke(runner, ['ls', '--jsonvja', '--title=Not created'])
        data = json.loads(res.output)
        assert len(data) == 0

    def test_task_filter_urgency(self, runner):
        res = invoke(runner, ['ls', '--jsonvja', '--urgency=10'])
        data = json.loads(res.output)
        assert len(data) > 0
        assert data[0]['urgency'] >= 10
        res = invoke(runner, ['ls', '--jsonvja', '--urgency=10000'])
        data = json.loads(res.output)
        assert len(data) == 0

    def test_task_custom_format(self, runner):
        res = invoke(runner, 'ls --custom-format=ids_only')
        for line in res.output:
            assert re.match(r'^\d*$', line)
