import configparser
import datetime
import json
import os
import re

import pytest
import requests
from dateutil import tz
from tests.conftest import invoke
from vja.model import RELATION_KINDS

ADD_SUCCESS_PATTERN = re.compile(r".*Created task (\d+) in project .*")
TODAY = datetime.datetime.now().replace(microsecond=0)
TODAY_ISO = TODAY.isoformat()
YESTERDAY = TODAY + datetime.timedelta(days=-1)
YESTERDAY_ISO = YESTERDAY.isoformat()
TOMORROW = TODAY + datetime.timedelta(days=1)
TOMORROW_ISO = TOMORROW.isoformat()
TOMORROW_AT_8_ISO = (TOMORROW.replace(hour=8, minute=0, second=0)).isoformat()
DATE_1 = TODAY + datetime.timedelta(days=10)
DATE_2 = DATE_1 + datetime.timedelta(days=1)
DATE_1_ISO = DATE_1.isoformat()
DATE_2_ISO = DATE_2.isoformat()


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


class TestEditGeneral:
    def test_edit_title(self, runner):
        before = json_for_task_id(runner, 1)
        new_title = f'{before["title"]}42'
        invoke(runner, ["edit", "1", "-i", f"{new_title}"])

        after = json_for_task_id(runner, 1)
        assert after["title"] == new_title
        assert after["updated"] >= before["updated"]
        # other attributes remain in place
        assert after["due_date"] == before["due_date"]
        assert after["reminders"] == before["reminders"]
        assert after["position"] == before["position"]
        assert after["project"]["id"] == before["project"]["id"]
        assert after["created"] == before["created"]

    def test_edit_due_date_with_time(self, runner):
        # edit due_date with iso timestamp
        invoke(runner, "edit 1 --due=2042-01-30T15:45:00-02:00")
        after = json_for_task_id(runner, 1)
        assert (
            after["due_date"]
            == datetime.datetime(2042, 1, 30, 15, 45, 0, tzinfo=tz.tzoffset(None, -2*3600))
            .astimezone(tz.tzlocal()).replace(tzinfo=None).isoformat()
        )

        # unset due_date
        before = json_for_task_id(runner, 1)
        assert before["due_date"] is not None
        invoke(runner, "edit 1 --due-date=")
        after = json_for_task_id(runner, 1)
        assert after["due_date"] is None

        # edit due_date with default time
        invoke(runner, "edit 1 --due=tomorrow")
        after = json_for_task_id(runner, 1)
        assert after["due_date"] == TOMORROW_AT_8_ISO

        # edit due_date with given time
        invoke(runner, ["edit", "1", "--due=tomorrow 15:00"])
        after = json_for_task_id(runner, 1)
        assert (
            after["due_date"]
            == (TOMORROW.replace(hour=15, minute=0, second=0)).isoformat()
        )

        # edit due_date without time
        invoke(runner, "edit 1 --due=today")
        after = json_for_task_id(runner, 1)
        assert (
            after["due_date"]
            == (TODAY.replace(hour=15, minute=0, second=0)).isoformat()
        )

    def test_toggle_label(self, runner):
        labels_0 = json_for_task_id(runner, 1)["label_objects"]
        invoke(runner, "edit 1 --label=tag1 --force-create")
        labels_1 = json_for_task_id(runner, 1)["label_objects"]
        invoke(runner, "edit 1 --label=tag1")
        labels_2 = json_for_task_id(runner, 1)["label_objects"]

        assert labels_0 != labels_1
        assert labels_0 == labels_2
        assert has_label_with_title(labels_0, "tag1") or has_label_with_title(
            labels_1, "tag1"
        )

    def test_append_note(self, runner):
        invoke(runner, "edit 1 --note=line1")
        note_1 = json_for_task_id(runner, 1)["description"]
        invoke(runner, "edit 1 --note-append=line2")
        note_2 = json_for_task_id(runner, 1)["description"]

        assert note_1 == "line1"
        assert note_2 == "line1\nline2"

    def test_edit_project(self, runner):
        invoke(runner, "project add another project")
        invoke(runner, "edit 1 --project-id=1")
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


class TestEditReminder:
    def test_set_reminder_to_absolute_value(self, runner):
        invoke(runner, f"edit 2 --reminder={DATE_1_ISO}")
        before = json_for_task_id(runner, 2)

        invoke(runner, f"edit 2 --due={DATE_1_ISO} --reminder={DATE_2_ISO}")

        after = json_for_task_id(runner, 2)
        assert before["reminders"][0]["reminder"] == DATE_1_ISO
        assert after["reminders"][0]["reminder"] == DATE_2_ISO
        assert not after["reminders"][0]["relative_to"]

    def test_set_reminder_to_due(self, runner):
        invoke(runner, f"edit 2 --reminder={DATE_1_ISO}")
        before = json_for_task_id(runner, 2)

        invoke(runner, f"edit 2 --due={DATE_2_ISO} --reminder=due")

        after = json_for_task_id(runner, 2)
        assert before["reminders"][0]["reminder"] == DATE_1_ISO
        assert after["reminders"][0]["reminder"] == DATE_2_ISO
        assert after["reminders"][0]["relative_period"] == 0
        assert after["reminders"][0]["relative_to"] == "due_date"

    def test_set_reminder_to_due_empty_option(self, runner):
        invoke(runner, f"edit 2 --reminder={DATE_1_ISO}")

        invoke(runner, f"edit 2 --due={DATE_2_ISO} --reminder")

        after = json_for_task_id(runner, 2)
        assert after["reminders"][0]["reminder"] == DATE_2_ISO
        assert after["reminders"][0]["relative_period"] == 0
        assert after["reminders"][0]["relative_to"] == "due_date"

    def test_set_reminder_to_relative_value(self, runner):
        invoke(runner, f"edit 2 --reminder={DATE_1_ISO}")

        invoke(
            runner,
            ["edit", "2", "--due={DATE_2_ISO}", "--reminder=1h1m before due_date"],
        )

        after = json_for_task_id(runner, 2)
        assert after["reminders"][0]["relative_period"] == -3660
        assert after["reminders"][0]["relative_to"] == "due_date"

    def test_unset_reminder(self, runner):
        invoke(runner, f"edit 2 --reminder={DATE_1_ISO}")
        before = json_for_task_id(runner, 2)

        invoke(runner, "edit 2 --reminder=")

        after = json_for_task_id(runner, 2)
        assert before["reminders"][0]["reminder"] == DATE_1_ISO
        assert not after["reminders"]


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
        invoke(runner, "edit 1 --priority=5")
        json_0 = json_for_task_id(runner, 1)
        invoke(runner, "check 1")
        json_1 = json_for_task_id(runner, 1)
        invoke(runner, "check 1")
        json_2 = json_for_task_id(runner, 1)
        assert json_0["priority"] == json_1["priority"] == json_2["priority"] == 5


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
        assert re.search(r"id: 1", res.output)
        assert re.search(r"id: 2", res.output)
        assert re.search(r"id: 3", res.output)


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


class TestDeleteTask:
    def test_delete_task(self, runner):
        res = invoke(runner, "add task to delete --force --project=test-project")
        task_id = ADD_SUCCESS_PATTERN.match(res.output).group(1)

        res = invoke(runner, f"delete {task_id}")
        assert res.exit_code == 0
        assert f"Deleted task {task_id}" in res.output

        invoke(runner, f"show {task_id}", expected_return_code=1)

    def test_delete_multiple_tasks(self, runner):
        task_ids = []
        for _ in range(2):
            res = invoke(runner, "add batch delete test --force --project=test-project")
            task_ids.append(ADD_SUCCESS_PATTERN.match(res.output).group(1))

        res = invoke(runner, f"delete {task_ids[0]} {task_ids[1]}")
        assert res.exit_code == 0
        for task_id in task_ids:
            assert f"Deleted task {task_id}" in res.output

        for task_id in task_ids:
            invoke(runner, f"show {task_id}", expected_return_code=1)

    def test_delete_nonexistent_task(self, runner):
        invoke(runner, "delete 99999", expected_return_code=1)


def json_for_created_task(runner, message):
    assert re.match(ADD_SUCCESS_PATTERN, message), message
    task_id = ADD_SUCCESS_PATTERN.findall(message)[0]
    return json_for_task_id(runner, task_id)


def json_for_task_id(runner, task_id):
    res = invoke(runner, f"show {task_id} --jsonvja")

    assert res.exit_code == 0, res
    data = json.loads(res.output)
    return data


def has_label_with_title(labels, title):
    label_titles = [x["title"] for x in labels]
    return title in label_titles


def has_assignee_with_username(assignees, username):
    return username in [x["username"] for x in assignees]


class TestRelationDisplay:
    def test_show_displays_relation_and_inverse(self, runner, subtask_relation):
        source = json_for_task_id(runner, 1)
        assert any(
            r["kind"] == "subtask" and r["other_task_id"] == 2
            for r in source["relations"]
        )
        target = json_for_task_id(runner, 2)
        assert any(
            r["kind"] == "parenttask" and r["other_task_id"] == 1
            for r in target["relations"]
        )

    def test_list_returns_relations(self, runner, subtask_relation):
        res = invoke(runner, "ls --jsonvja")
        tasks = json.loads(res.output)
        task_1 = next(task for task in tasks if task["id"] == 1)
        assert any(r["other_task_id"] == 2 for r in task_1["relations"])

    def test_list_shows_relation_flag(self, runner, subtask_relation):
        lines = invoke(runner, "ls").output.splitlines()
        task_1_line = next(line for line in lines if line.strip().startswith("1 ("))
        task_3_line = next(line for line in lines if line.strip().startswith("3 ("))
        # task 1 has a relation, task 3 does not -> only task 1 shows the "L" flag
        assert "L" in task_1_line
        assert "L" not in task_3_line


@pytest.fixture(name="subtask_relation")
def _subtask_relation():
    _delete_relation_if_exists(1, "subtask", 2)
    _put_relation(1, "subtask", 2)
    yield
    _delete_relation_if_exists(1, "subtask", 2)


def _put_relation(task_id, relation_kind, other_task_id):
    _api_request(
        "PUT",
        f"/tasks/{task_id}/relations",
        {"other_task_id": other_task_id, "relation_kind": relation_kind},
    )


def _delete_relation(task_id, relation_kind, other_task_id):
    _api_request("DELETE", f"/tasks/{task_id}/relations/{relation_kind}/{other_task_id}")


def _delete_relation_if_exists(task_id, relation_kind, other_task_id):
    try:
        _delete_relation(task_id, relation_kind, other_task_id)
    except requests.HTTPError as error:
        if error.response.status_code != 404:
            raise


def _api_request(method, path, json_body=None):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.environ["VJA_CONFIGDIR"], "config.rc"))
    api_url = config["application"]["api_url"]
    with open(
        os.path.join(os.environ["VJA_CONFIGDIR"], "token.json"), encoding="utf-8"
    ) as token_file:
        token = json.load(token_file)["token"]
    response = requests.request(
        method,
        f"{api_url}{path}",
        headers={"Authorization": f"Bearer {token}"},
        json=json_body,
        timeout=30,
    )
    response.raise_for_status()
    return response


class TestRelation:
    def test_add_creates_relation_and_inverse(self, runner, relation_cleanup):
        relation_cleanup.append((1, "subtask", 2))
        res = invoke(runner, "relation add 1 subtask 2")
        assert res.exit_code == 0
        source = json_for_task_id(runner, 1)
        assert any(
            r["kind"] == "subtask" and r["other_task_id"] == 2
            for r in source["relations"]
        )
        target = json_for_task_id(runner, 2)
        assert any(
            r["kind"] == "parenttask" and r["other_task_id"] == 1
            for r in target["relations"]
        )

    def test_remove_removes_relation_and_inverse(self, runner, relation_cleanup):
        relation_cleanup.append((1, "subtask", 2))
        assert invoke(runner, "relation add 1 subtask 2").exit_code == 0
        assert invoke(runner, "relation remove 1 subtask 2").exit_code == 0
        source = json_for_task_id(runner, 1)
        assert not any(
            r["kind"] == "subtask" and r["other_task_id"] == 2
            for r in source["relations"]
        )
        target = json_for_task_id(runner, 2)
        assert not any(
            r["kind"] == "parenttask" and r["other_task_id"] == 1
            for r in target["relations"]
        )

    def test_blocking_creates_blocked_inverse(self, runner, relation_cleanup):
        relation_cleanup.append((1, "blocking", 3))
        res = invoke(runner, "relation add 1 blocking 3")
        assert res.exit_code == 0
        source = json_for_task_id(runner, 1)
        assert any(
            r["kind"] == "blocking" and r["other_task_id"] == 3
            for r in source["relations"]
        )
        target = json_for_task_id(runner, 3)
        assert any(
            r["kind"] == "blocked" and r["other_task_id"] == 1
            for r in target["relations"]
        )

    def test_related_is_symmetric(self, runner, relation_cleanup):
        relation_cleanup.append((1, "related", 2))
        res = invoke(runner, "relation add 1 related 2")
        assert res.exit_code == 0
        source = json_for_task_id(runner, 1)
        assert any(
            r["kind"] == "related" and r["other_task_id"] == 2
            for r in source["relations"]
        )
        target = json_for_task_id(runner, 2)
        assert any(
            r["kind"] == "related" and r["other_task_id"] == 1
            for r in target["relations"]
        )

    @pytest.mark.parametrize("relation_kind", RELATION_KINDS)
    def test_every_kind_round_trips(self, runner, relation_kind, relation_cleanup):
        relation_cleanup.append((1, relation_kind, 2))
        assert invoke(runner, f"relation add 1 {relation_kind} 2").exit_code == 0
        relations = json_for_task_id(runner, 1)["relations"]
        assert any(
            r["kind"] == relation_kind and r["other_task_id"] == 2 for r in relations
        )
        assert invoke(runner, f"relation rm 1 {relation_kind} 2").exit_code == 0

    def test_verbose_show_displays_relation(self, runner, relation_cleanup):
        relation_cleanup.append((1, "subtask", 2))
        res = invoke(runner, "relation add 1 subtask 2 -v")
        assert "Modified task 1 in project" in res.output
        assert "subtask" in res.output

    def test_invalid_kind_is_rejected(self, runner):
        invoke(runner, "relation add 1 bogus 2", expected_return_code=2)

    def test_self_relation_is_rejected(self, runner):
        invoke(runner, "relation add 1 subtask 1", expected_return_code=1)

    @pytest.mark.parametrize("remove_verb", ["remove", "rm", "delete"])
    def test_remove_nonexistent_relation_is_rejected(self, runner, remove_verb):
        # each verb must resolve to the removal command (exit 1 = server rejection),
        # not fall through to "No such command" (exit 2)
        invoke(runner, f"relation {remove_verb} 1 subtask 3", expected_return_code=1)


@pytest.fixture(name="relation_cleanup")
def _relation_cleanup():
    created = []
    yield created
    for task_id, relation_kind, other_task_id in created:
        try:
            _delete_relation(task_id, relation_kind, other_task_id)
        except requests.HTTPError as error:
            if error.response.status_code != 404:
                raise
