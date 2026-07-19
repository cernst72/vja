from tests.conftest import invoke
from tests.test_command_helpers import json_for_created_task, json_for_task_id


class TestCloneTask:
    def test_clone_task(self, runner):
        before = json_for_task_id(runner, 1)
        res = invoke(runner, "clone 1 title of new task cloned from 1")
        after = json_for_created_task(runner, res.output)
        assert after["project"] == before["project"]
        assert after["due_date"] == before["due_date"]
        assert after["label_objects"] == before["label_objects"]
        assert after["title"] != before["title"]
        assert after["id"] != before["id"]
        assert after["created"] != before["created"]
