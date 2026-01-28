import json
import re

from tests.conftest import invoke


class TestUser:
    def test_user_show(self, runner):
        res = invoke(runner, "user show")
        assert re.search(r"username=\'test\'", res.output)

    def test_user_show_json(self, runner):
        res = invoke(runner, "user show --json")
        assert json.loads(res.output)["username"] == "test"

    def test_user_show_jsonvja(self, runner):
        res = invoke(runner, "user show --jsonvja")
        assert json.loads(res.output)["username"] == "test"


class TestProject:
    def test_project_ls(self, runner):
        res = invoke(runner, "project ls")
        assert re.search(r"test-project", res.output)

    def test_project_show(self, runner):
        res = invoke(runner, "project show 1")
        assert len(res.output) > 0

    def test_project_ls_custom_format(self, runner):
        res = invoke(runner, "project ls --custom-format=ids_only")
        for line in res.output:
            assert re.match(r"^-?\d*$", line)


class TestBucket:
    def test_bucket_ls(self, runner):
        res = invoke(runner, "bucket ls --project-id=1")
        assert re.search(r"To-Do|Backlog", res.output)

    def test_bucket_ls_custom_format(self, runner):
        res = invoke(runner, "bucket ls --project-id=1 --custom-format=ids_only")
        for line in res.output:
            assert re.match(r"^\d*$", line)


class TestLabel:
    def test_label_ls(self, runner):
        res = invoke(runner, "label ls")
        assert re.search(r"my_tag", res.output)

    def test_label_ls_custom_format(self, runner):
        res = invoke(runner, "label ls --custom-format=ids_only")
        for line in res.output:
            assert re.match(r"^\d*$", line)


class TestSingleTask:
    def test_task_show(self, runner):
        res = invoke(runner, "show 1")
        assert re.search(r"id: 1", res.output)

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


class TestTaskLs:
    def test_task_ls(self, runner, use_old_api):
        res = invoke(runner, "ls", use_old_api)
        assert re.search(r"At least one task", res.output)

    def test_task_ls_json(self, runner, use_old_api):
        res = invoke(runner, "ls --json", use_old_api)
        assert json.loads(res.output)[0]["title"] is not None

    def test_task_ls_jsonvja(self, runner, use_old_api):
        res = invoke(runner, "ls --jsonvja", use_old_api)
        data = json.loads(res.output)[0]
        assert data["title"] is not None

    def test_filter_id(self, runner, use_old_api):
        res = invoke(runner, ["ls", "--jsonvja", "2"], use_old_api)
        data = json.loads(res.output)
        assert data[0]["id"] == 2
        res = invoke(runner, ["ls", "--jsonvja", "1", "2"], use_old_api)
        data = json.loads(res.output)
        assert len(data) == 2
        assert data[0]["id"] in [1, 2]
        assert data[1]["id"] in [1, 2]

    def test_sort_id(self, runner, use_old_api):
        res = invoke(runner, ["ls", "--jsonvja", "--sort=id"], use_old_api)
        data = json.loads(res.output)
        assert data[0]["id"] == 1
        res = invoke(runner, ["ls", "--jsonvja", "--sort=-id"], use_old_api)
        data = json.loads(res.output)
        assert data[0]["id"] > 1

    def test_sort_combined(self, runner, use_old_api):
        res = invoke(
            runner,
            [
                "ls",
                "--jsonvja",
                "--sort=due_date, is_favorite, -priority, project.title",
            ], use_old_api
        )
        data = json.loads(res.output)
        assert data[0]["due_date"] is not None
        assert data[-1]["due_date"] is None

    def test_task_custom_format(self, runner, use_old_api):
        res = invoke(runner, "ls --custom-format=ids_only", use_old_api)
        for line in res.output:
            assert re.match(r"^\d*$", line)

    def test_task_custom_format_long(self, runner, use_old_api):
        res = invoke(runner, "ls --custom-format=tasklist_long", use_old_api)
        assert re.search(r"At least one task", res.output)


class TestTaskLsFilter:
    def test_task_filter_due(self, runner, use_old_api):
        res = invoke(runner, ["ls", "--jsonvja", "--due-date=after yesterday"], use_old_api)
        data = json.loads(res.output)
        assert len(data) > 0
        res = invoke(runner, ["ls", "--jsonvja", "--due-date=before tomorrow"], use_old_api)
        data = json.loads(res.output)
        assert len(data) > 0
        res = invoke(runner, ["ls", "--jsonvja", "--due-date=after next week"], use_old_api)
        data = json.loads(res.output)
        assert len(data) == 0
        res = invoke(runner, ["ls", "--jsonvja", "--due-date=" """"""], use_old_api)
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(i["due_date"] is None for i in data)

    def test_task_filter_favorite(self, runner, use_old_api):
        res = invoke(runner, ["ls", "--jsonvja", "--favorite=True"], use_old_api)
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(i["is_favorite"] for i in data)

    def test_task_filter_label(self, runner, use_old_api):
        res = invoke(runner, ["ls", "--jsonvja", "--label=y_ta"], use_old_api)
        data = json.loads(res.output)
        assert len(data) > 0
        assert data[0]["label_objects"][0]["title"] == "my_tag"
        res = invoke(runner, ["ls", "--jsonvja", "--label=unknown_label"], use_old_api)
        data = json.loads(res.output)
        assert len(data) == 0

    def test_task_filter_label_empty(self, runner, use_old_api):
        res = invoke(runner, ["ls", "--jsonvja", "--label=" """"""], use_old_api)
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(len(i["label_objects"]) == 0 for i in data)

    def test_task_filter_project(self, runner, use_old_api):
        res = invoke(runner, ["ls", "--jsonvja", "--project=est-project"], use_old_api)
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(i["project"]["title"] == "test-project" for i in data)
        res = invoke(runner, ["ls", "--jsonvja", "--project=Not created"], use_old_api)
        data = json.loads(res.output)
        assert len(data) == 0

    def test_task_filter_base_project(self, runner, use_old_api):
        res = invoke(runner, ["ls", "--jsonvja", "--base-project=est-project"], use_old_api)
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(
            i["project"]["title"] == "test-project"
            or i["project"]["title"] == "grand-child"
            for i in data
        )
        assert any(i["project"]["title"] == "test-project" for i in data)
        assert any(i["project"]["title"] == "grand-child" for i in data)
        res = invoke(runner, ["ls", "--jsonvja", "--project=Not created"], use_old_api)
        data = json.loads(res.output)
        assert len(data) == 0

    def test_task_filter_priority(self, runner, use_old_api):
        res = invoke(runner, ["ls", "--jsonvja", "--priority=eq 5"], use_old_api)
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(i["priority"] == 5 for i in data)
        res = invoke(runner, ["ls", "--jsonvja", "--priority=gt 4"], use_old_api)
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(i["priority"] > 4 for i in data)
        res = invoke(runner, ["ls", "--jsonvja", "--priority=gt 5"], use_old_api)
        data = json.loads(res.output)
        assert len(data) == 0

    def test_task_filter_title(self, runner, use_old_api):
        res = invoke(runner, ["ls", "--jsonvja", "--title=at least"], use_old_api)
        data = json.loads(res.output)
        assert len(data) > 0
        assert all("At least one task" in i["title"] for i in data)
        res = invoke(runner, ["ls", "--jsonvja", "--title=Not created"], use_old_api)
        data = json.loads(res.output)
        assert len(data) == 0

    def test_task_filter_urgency(self, runner, use_old_api):
        res = invoke(runner, ["ls", "--jsonvja", "--urgency=10"], use_old_api)
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(i["urgency"] >= 10 for i in data)
        res = invoke(runner, ["ls", "--jsonvja", "--urgency=10000"], use_old_api)
        data = json.loads(res.output)
        assert len(data) == 0

    def test_task_filter_general(self, runner, use_old_api):
        res = invoke(runner, ["ls", "--jsonvja", "--filter=due_date after 2 days ago"], use_old_api)
        assert len(json.loads(res.output)) > 0
        res = invoke(runner, ["ls", "--jsonvja", "--filter=due_date after 200 days"], use_old_api)
        assert len(json.loads(res.output)) == 0
        res = invoke(runner, ["ls", "--jsonvja", "--filter=due_date after 200 days"], use_old_api)
        assert len(json.loads(res.output)) == 0
        res = invoke(runner, ["ls", "--jsonvja", "--filter=is_favorite eq True"], use_old_api)
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(i["is_favorite"] for i in data)
        res = invoke(runner, ["ls", "--jsonvja", "--filter=priority gt 2"], use_old_api)
        assert len(json.loads(res.output)) > 0
        res = invoke(runner, ["ls", "--jsonvja", "--filter=priority gt 5"], use_old_api)
        assert len(json.loads(res.output)) == 0
        res = invoke(
            runner, ["ls", "--jsonvja", "--filter=title contains At least one"], use_old_api
        )
        assert len(json.loads(res.output)) > 0
        res = invoke(
            runner, ["ls", "--jsonvja", "--filter=title contains TASK_NOT_CREATED"], use_old_api
        )
        assert len(json.loads(res.output)) == 0

    def test_task_filter_general_label(self, runner, use_old_api):
        res = invoke(runner, ["ls", "--jsonvja", "--filter=labels contains my_tag"], use_old_api)
        data = json.loads(res.output)
        assert len(data) > 0
        assert all("my_tag" in _labels_from_task_json(task) for task in data)
        res = invoke(runner, ["ls", "--jsonvja", "--filter=labels ne my_tag"], use_old_api)
        data = json.loads(res.output)
        assert len(data) > 0
        assert all("my_tag" not in _labels_from_task_json(task) for task in data)

    def test_task_filter_general_combined(self, runner, use_old_api):
        res = invoke(
            runner, ["ls", "--jsonvja", "--filter=id gt 0", "--filter=id lt 2"], use_old_api
        )
        data = json.loads(res.output)
        assert len(data) == 1
        assert all(i["id"] == 1 for i in data)


def _labels_from_task_json(task):
    return " ".join(label["title"] for label in task["label_objects"] or [])
