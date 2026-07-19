import json

from tests.conftest import invoke


class TestTaskLsFilter:
    def test_task_filter_due(self, runner):
        res = invoke(runner, ["ls", "--jsonvja", "--due-date=after yesterday"])
        data = json.loads(res.output)
        assert len(data) > 0
        res = invoke(runner, ["ls", "--jsonvja", "--due-date=before tomorrow"])
        data = json.loads(res.output)
        assert len(data) > 0
        res = invoke(runner, ["ls", "--jsonvja", "--due-date=after next week"])
        data = json.loads(res.output)
        assert len(data) == 0
        res = invoke(runner, ["ls", "--jsonvja", "--due-date="])
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(i["due_date"] is None for i in data)

    def test_task_filter_favorite(self, runner):
        res = invoke(runner, ["ls", "--jsonvja", "--favorite=True"])
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(i["is_favorite"] for i in data)

    def test_task_filter_label(self, runner):
        res = invoke(runner, ["ls", "--jsonvja", "--label=y_ta"])
        data = json.loads(res.output)
        assert len(data) > 0
        assert data[0]["label_objects"][0]["title"] == "my_tag"
        res = invoke(runner, ["ls", "--jsonvja", "--label=unknown_label"])
        data = json.loads(res.output)
        assert len(data) == 0

    def test_task_filter_label_empty(self, runner):
        res = invoke(runner, ["ls", "--jsonvja", "--label="])
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(len(i["label_objects"]) == 0 for i in data)

    def test_task_filter_project(self, runner):
        res = invoke(runner, ["ls", "--jsonvja", "--project=est-project"])
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(i["project"]["title"] == "test-project" for i in data)
        res = invoke(runner, ["ls", "--jsonvja", "--project=Not created"])
        data = json.loads(res.output)
        assert len(data) == 0

    def test_task_filter_base_project(self, runner):
        res = invoke(runner, ["ls", "--jsonvja", "--base-project=est-project"])
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(
            i["project"]["title"] == "test-project"
            or i["project"]["title"] == "grand-child"
            for i in data
        )
        assert any(i["project"]["title"] == "test-project" for i in data)
        assert any(i["project"]["title"] == "grand-child" for i in data)
        res = invoke(runner, ["ls", "--jsonvja", "--project=Not created"])
        data = json.loads(res.output)
        assert len(data) == 0

    def test_task_filter_priority(self, runner):
        res = invoke(runner, ["ls", "--jsonvja", "--priority=eq 5"])
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(i["priority"] == 5 for i in data)
        res = invoke(runner, ["ls", "--jsonvja", "--priority=gt 4"])
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(i["priority"] > 4 for i in data)
        res = invoke(runner, ["ls", "--jsonvja", "--priority=gt 5"])
        data = json.loads(res.output)
        assert len(data) == 0

    def test_task_filter_title(self, runner):
        res = invoke(runner, ["ls", "--jsonvja", "--title=at least"])
        data = json.loads(res.output)
        assert len(data) > 0
        assert all("At least one task" in i["title"] for i in data)
        res = invoke(runner, ["ls", "--jsonvja", "--title=Not created"])
        data = json.loads(res.output)
        assert len(data) == 0

    def test_task_filter_bucket(self, runner):
        res = invoke(runner, ["ls", "--jsonvja", "--bucket=1"])
        data = json.loads(res.output)
        assert len(data) > 0

    def test_task_filter_urgency(self, runner):
        res = invoke(runner, ["ls", "--jsonvja", "--urgency=10"])
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(i["urgency"] >= 10 for i in data)
        res = invoke(runner, ["ls", "--jsonvja", "--urgency=10000"])
        data = json.loads(res.output)
        assert len(data) == 0

    def test_task_filter_general(self, runner):
        res = invoke(runner, ["ls", "--jsonvja", "--filter=due_date after 2 days ago"])
        assert len(json.loads(res.output)) > 0
        res = invoke(runner, ["ls", "--jsonvja", "--filter=due_date after 200 days"])
        assert len(json.loads(res.output)) == 0
        res = invoke(runner, ["ls", "--jsonvja", "--filter=due_date after 200 days"])
        assert len(json.loads(res.output)) == 0
        res = invoke(runner, ["ls", "--jsonvja", "--filter=is_favorite eq True"])
        data = json.loads(res.output)
        assert len(data) > 0
        assert all(i["is_favorite"] for i in data)
        res = invoke(runner, ["ls", "--jsonvja", "--filter=priority gt 2"])
        assert len(json.loads(res.output)) > 0
        res = invoke(runner, ["ls", "--jsonvja", "--filter=priority gt 5"])
        assert len(json.loads(res.output)) == 0
        res = invoke(
            runner, ["ls", "--jsonvja", "--filter=title contains At least one"]
        )
        assert len(json.loads(res.output)) > 0
        res = invoke(
            runner, ["ls", "--jsonvja", "--filter=title contains TASK_NOT_CREATED"]
        )
        assert len(json.loads(res.output)) == 0

    def test_task_filter_general_label(self, runner):
        res = invoke(runner, ["ls", "--jsonvja", "--filter=labels contains my_tag"])
        data = json.loads(res.output)
        assert len(data) > 0
        assert all("my_tag" in _labels_from_task_json(task) for task in data)
        res = invoke(runner, ["ls", "--jsonvja", "--filter=labels ne my_tag"])
        data = json.loads(res.output)
        assert len(data) > 0
        assert all("my_tag" not in _labels_from_task_json(task) for task in data)

    def test_task_filter_general_combined(self, runner):
        res = invoke(
            runner, ["ls", "--jsonvja", "--filter=id gt 0", "--filter=id lt 2"]
        )
        data = json.loads(res.output)
        assert len(data) == 1
        assert all(i["id"] == 1 for i in data)


def _labels_from_task_json(task):
    return " ".join(label["title"] for label in task["label_objects"] or [])
