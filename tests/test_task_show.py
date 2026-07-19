import json
import re

from tests.conftest import invoke


class TestSingleTask:
    def test_task_show(self, runner):
        res = invoke(runner, "show 1")
        assert re.search(r"id: 1", res.output)
        assert res.output

    def test_task_show_json(self, runner):
        res = invoke(runner, "show 1 --json")
        assert json.loads(res.output)["id"] == 1

    def test_task_show_jsonvja(self, runner):
        res = invoke(runner, "show 1 --jsonvja")
        data = json.loads(res.output)
        assert data["id"] == 1
        assert data["title"] is not None
        assert data["project"]["id"] is not None
        assert data["created"] is not None
        assert data["updated"] is not None
        assert data["bucket_objects"] is not None
        assert data["label_objects"] is not None
