import json
import re

from tests.conftest import invoke


class TestTaskLs:
    def test_task_ls(self, runner):
        res = invoke(runner, "ls")
        assert re.search(r"At least one task", res.output)

    def test_task_ls_json(self, runner):
        res = invoke(runner, "ls --json")
        assert json.loads(res.output)[0]["title"] is not None

    def test_task_ls_jsonvja(self, runner):
        res = invoke(runner, "ls --jsonvja")
        data = json.loads(res.output)[0]
        assert data["title"] is not None

    def test_filter_id(self, runner):
        res = invoke(runner, ["ls", "--jsonvja", "2"])
        data = json.loads(res.output)
        assert data[0]["id"] == 2
        res = invoke(runner, ["ls", "--jsonvja", "1", "2"])
        data = json.loads(res.output)
        assert len(data) == 2
        assert data[0]["id"] in [1, 2]
        assert data[1]["id"] in [1, 2]

    def test_sort_id(self, runner):
        res = invoke(runner, ["ls", "--jsonvja", "--sort=id"])
        data = json.loads(res.output)
        assert data[0]["id"] == 1
        res = invoke(runner, ["ls", "--jsonvja", "--sort=-id"])
        data = json.loads(res.output)
        assert data[0]["id"] > 1

    def test_sort_combined(self, runner):
        res = invoke(
            runner,
            [
                "ls",
                "--jsonvja",
                "--sort=due_date, is_favorite, -priority, project.title",
            ],
        )
        data = json.loads(res.output)
        assert data[0]["due_date"] is not None
        assert data[-1]["due_date"] is None

    def test_task_custom_format(self, runner):
        res = invoke(runner, "ls --custom-format=ids_only")
        for line in res.output:
            assert re.match(r"^\d*$", line)

    def test_task_custom_format_long(self, runner):
        res = invoke(runner, "ls --custom-format=tasklist_long")
        assert re.search(r"At least one task", res.output)
