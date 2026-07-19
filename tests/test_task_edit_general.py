import datetime

from dateutil import tz

from tests.conftest import invoke
from tests.test_command_helpers import (
    TODAY,
    TODAY_ISO,
    TOMORROW,
    TOMORROW_AT_8_ISO,
    has_label_with_title,
    json_for_task_id,
)


class TestEditGeneral:
    def test_edit_title(self, runner):
        before = json_for_task_id(runner, 1)
        new_title = f'{before["title"]}42'
        invoke(runner, ["edit", "1", "-i", f"{new_title}"])

        after = json_for_task_id(runner, 1)
        assert after["title"] == new_title
        assert after["updated"] >= before["updated"]
        assert after["due_date"] == before["due_date"]
        assert after["reminders"] == before["reminders"]
        assert after["position"] == before["position"]
        assert after["project"]["id"] == before["project"]["id"]
        assert after["created"] == before["created"]

    def test_edit_due_date_with_time(self, runner):
        invoke(runner, "edit 1 --due=2042-01-30T15:45:00-02:00")
        after = json_for_task_id(runner, 1)
        assert (
            after["due_date"]
            == datetime.datetime(2042, 1, 30, 15, 45, 0, tzinfo=tz.tzoffset(None, -2 * 3600))
            .astimezone(tz.tzlocal())
            .replace(tzinfo=None)
            .isoformat()
        )

        before = json_for_task_id(runner, 1)
        assert before["due_date"] is not None
        invoke(runner, "edit 1 --due-date=")
        after = json_for_task_id(runner, 1)
        assert after["due_date"] is None

        invoke(runner, "edit 1 --due=tomorrow")
        after = json_for_task_id(runner, 1)
        assert after["due_date"] == TOMORROW_AT_8_ISO

        invoke(runner, ["edit", "1", "--due=tomorrow 15:00"])
        after = json_for_task_id(runner, 1)
        assert after["due_date"] == (TOMORROW.replace(hour=15, minute=0, second=0)).isoformat()

        invoke(runner, "edit 1 --due=today")
        after = json_for_task_id(runner, 1)
        assert after["due_date"] == (TODAY.replace(hour=15, minute=0, second=0)).isoformat()

    def test_toggle_label(self, runner):
        labels_0 = json_for_task_id(runner, 1)["label_objects"]
        invoke(runner, "edit 1 --label=tag1 --force-create")
        labels_1 = json_for_task_id(runner, 1)["label_objects"]
        invoke(runner, "edit 1 --label=tag1")
        labels_2 = json_for_task_id(runner, 1)["label_objects"]

        assert labels_0 != labels_1
        assert labels_0 == labels_2
        assert has_label_with_title(labels_0, "tag1") or has_label_with_title(labels_1, "tag1")

    def test_append_note(self, runner):
        invoke(runner, "edit 1 --note=line1")
        note_1 = json_for_task_id(runner, 1)["description"]
        invoke(runner, "edit 1 --note-append=line2")
        note_2 = json_for_task_id(runner, 1)["description"]

        assert note_1 == "line1"
        assert note_2 == "line1\nline2"

    def test_edit_project(self, runner):
        invoke(runner, "project add another project")
        invoke(runner, "edit 1 --project-id=Inbox")
        project_1 = json_for_task_id(runner, 1)["project"]["id"]
        invoke(runner, "edit 1 -o 2")
        project_2 = json_for_task_id(runner, 1)["project"]["id"]

        assert project_1 == 1
        assert project_2 == 2

    def test_toggle_favorite(self, runner):
        invoke(runner, "edit 1 --star")
        favorite_0 = json_for_task_id(runner, 1)["is_favorite"]
        invoke(runner, "edit 1 --no-star")
        favorite_1 = json_for_task_id(runner, 1)["is_favorite"]
        invoke(runner, "edit 1 --star")
        favorite_2 = json_for_task_id(runner, 1)["is_favorite"]

        assert favorite_0 != favorite_1
        assert favorite_0 == favorite_2
