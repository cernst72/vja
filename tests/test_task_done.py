from tests.conftest import invoke
from tests.test_command_helpers import edit_task, json_for_task_id


class TestToggleDoneTask:
    def test_toggle_done(self, runner):
        done_0 = json_for_task_id(runner, 1)["done"]
        invoke(runner, "check 1")
        done_1 = json_for_task_id(runner, 1)["done"]
        invoke(runner, "check 1")
        done_2 = json_for_task_id(runner, 1)["done"]
        assert done_0 != done_1
        assert done_0 == done_2

    def test_toggle_does_not_modify_other_fields(self, runner):
        json_0 = edit_task(runner, 1, "--priority=5")
        invoke(runner, "check 1")
        json_1 = json_for_task_id(runner, 1)
        invoke(runner, "check 1")
        json_2 = json_for_task_id(runner, 1)
        assert json_0["priority"] == json_1["priority"] == json_2["priority"] == 5
