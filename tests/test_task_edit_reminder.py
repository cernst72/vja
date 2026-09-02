from tests.conftest import invoke
from tests.test_command_helpers import DATE_1_ISO, DATE_2_ISO, edit_task, json_for_task_id


class TestEditReminder:
    def test_set_reminder_to_absolute_value(self, runner):
        invoke(runner, f"edit 2 --reminder={DATE_1_ISO}")
        before = json_for_task_id(runner, 2)

        after = edit_task(runner, 2, f"--due={DATE_1_ISO}", f"--reminder={DATE_2_ISO}")
        assert before["reminders"][0]["reminder"] == DATE_1_ISO
        assert after["reminders"][0]["reminder"] == DATE_2_ISO
        assert not after["reminders"][0]["relative_to"]

    def test_set_reminder_to_due(self, runner):
        invoke(runner, f"edit 2 --reminder={DATE_1_ISO}")
        before = json_for_task_id(runner, 2)

        after = edit_task(runner, 2, f"--due={DATE_2_ISO}", "--reminder=due")
        assert before["reminders"][0]["reminder"] == DATE_1_ISO
        assert after["reminders"][0]["reminder"] == DATE_2_ISO
        assert after["reminders"][0]["relative_period"] == 0
        assert after["reminders"][0]["relative_to"] == "due_date"

    def test_set_reminder_to_due_empty_option(self, runner):
        invoke(runner, f"edit 2 --reminder={DATE_1_ISO}")

        after = edit_task(runner, 2, f"--due={DATE_2_ISO}", "--reminder")
        assert after["reminders"][0]["reminder"] == DATE_2_ISO
        assert after["reminders"][0]["relative_period"] == 0
        assert after["reminders"][0]["relative_to"] == "due_date"

    def test_set_reminder_to_relative_value(self, runner):
        invoke(runner, f"edit 2 --reminder={DATE_1_ISO}")

        after = edit_task(runner, 2, f"--due={DATE_2_ISO}", "--reminder=1h1m before due_date")
        assert after["reminders"][0]["relative_period"] == -3660
        assert after["reminders"][0]["relative_to"] == "due_date"

    def test_unset_reminder(self, runner):
        invoke(runner, f"edit 2 --reminder={DATE_1_ISO}")
        before = json_for_task_id(runner, 2)

        after = edit_task(runner, 2, "--reminder=")
        assert before["reminders"][0]["reminder"] == DATE_1_ISO
        assert not after["reminders"]
