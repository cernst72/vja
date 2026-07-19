from tests.conftest import invoke
from tests.test_command_helpers import (
    DATE_2_ISO,
    TOMORROW_AT_8_ISO,
    has_assignee_with_username,
    has_label_with_title,
    json_for_created_task,
)


class TestAddTask:
    def test_project_id(self, runner):
        res = invoke(runner, "add title of new task --force --project=1")
        after = json_for_created_task(runner, res.output)
        assert after["project"]["id"] == 1

    def test_project_title(self, runner):
        res = invoke(runner, "add title of new task --force --project=test-project")
        after = json_for_created_task(runner, res.output)
        assert after["project"]["title"] == "test-project"

    def test_due_date(self, runner):
        res = invoke(runner, "add title of new task --force --due=tomorrow")
        after = json_for_created_task(runner, res.output)
        assert after["due_date"] == TOMORROW_AT_8_ISO

    def test_duplicate_task_title_rejected(self, runner):
        invoke(runner, "add title of new task", 1, catch_exceptions=True)

    def test_default_reminder_uses_due(self, runner):
        res = invoke(
            runner,
            "add title of new task --force --project=test-project --due=today --reminder",
        )
        after = json_for_created_task(runner, res.output)
        assert after["reminders"][0]["relative_period"] == 0
        assert after["reminders"][0]["relative_to"] == "due_date"

    def test_default_reminder_with_absolute_time(self, runner):
        res = invoke(
            runner,
            f"add title of new task --force --project=test-project --reminder={DATE_2_ISO}",
        )
        after = json_for_created_task(runner, res.output)
        assert after["reminders"][0]["reminder"] == DATE_2_ISO

    def test_add_with_multiple_labels(self, runner):
        res = invoke(runner, "add multi labels --force -l tag_1 -l tag_2")
        after = json_for_created_task(runner, res.output)
        assert has_label_with_title(after["label_objects"], "tag_1")
        assert has_label_with_title(after["label_objects"], "tag_2")

    def test_add_with_assignee(self, runner):
        res = invoke(runner, "add task with assignee --force -A test")
        after = json_for_created_task(runner, res.output)
        assert has_assignee_with_username(after["assignee_objects"], "test")
