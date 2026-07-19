import datetime

from tests.conftest import invoke
from tests.test_command_helpers import TODAY_ISO, json_for_task_id


class TestMultipleTasks:
    def test_edit_three_tasks(self, runner):
        invoke(runner, "edit 1 2 3 --priority=4")
        for i in range(1, 4):
            after = json_for_task_id(runner, i)
            assert after["priority"] == 4
            assert after["updated"][:10] == TODAY_ISO[:10]
        invoke(runner, "edit 1 2 3 --priority=5")

    def test_show_three_tasks(self, runner):
        res = invoke(runner, "show 1 2 3")
        assert "id: 1" in res.output
        assert "id: 2" in res.output
        assert "id: 3" in res.output
