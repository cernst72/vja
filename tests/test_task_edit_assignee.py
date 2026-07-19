from tests.conftest import invoke
from tests.test_command_helpers import has_assignee_with_username, json_for_task_id


class TestEditAssignee:
    def test_toggle_assignee(self, runner):
        assignees_0 = json_for_task_id(runner, 1)["assignee_objects"]
        invoke(runner, "edit 1 --assignee=test")
        assignees_1 = json_for_task_id(runner, 1)["assignee_objects"]
        invoke(runner, "edit 1 --assignee=test")
        assignees_2 = json_for_task_id(runner, 1)["assignee_objects"]

        assert assignees_0 != assignees_1
        assert has_assignee_with_username(assignees_1, "test")
        assert not has_assignee_with_username(assignees_2, "test")
        assert assignees_0 == assignees_2
