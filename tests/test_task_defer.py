from tests.conftest import invoke
from tests.test_command_helpers import DATE_1_ISO, DATE_2_ISO, TOMORROW_ISO, YESTERDAY_ISO, json_for_task_id


class TestDeferTask:
    def test_defer_due_date_and_reminder(self, runner):
        invoke(runner, f"edit 2 --due-date={DATE_1_ISO} --reminder={DATE_1_ISO}")

        invoke(runner, "defer 2 1d")

        after = json_for_task_id(runner, 2)
        assert after["due_date"] == DATE_2_ISO
        assert after["reminders"][0]["reminder"] == DATE_2_ISO

    def test_dont_defer_relative_reminder(self, runner):
        invoke(runner, f"edit 2 --due-date={DATE_1_ISO} -r")

        invoke(runner, "defer 2 1d")

        after = json_for_task_id(runner, 2)
        assert after["due_date"] == DATE_2_ISO
        assert after["reminders"][0]["relative_period"] == 0
        assert after["reminders"][0]["relative_to"] == "due_date"

    def test_defer_past_due_relative_to_now(self, runner):
        invoke(runner, f"edit 2 --due-date={YESTERDAY_ISO}")

        invoke(runner, "defer 2 1d")

        after = json_for_task_id(runner, 2)
        assert after["due_date"][:10] == TOMORROW_ISO[:10]
