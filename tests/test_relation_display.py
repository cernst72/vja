import json
import re

from tests.conftest import invoke


class TestRelationDisplay:
    def test_show_displays_relation_and_inverse(self, runner):
        res = invoke(runner, "show 1")
        assert re.search(r"related: id=2", res.output)
        res = invoke(runner, "show 2")
        assert re.search(r"related: id=1", res.output)

    def test_list_returns_relations(self, runner):
        res = invoke(runner, "ls --jsonvja")
        tasks = json.loads(res.output)
        task_1 = next(task for task in tasks if task["id"] == 1)
        assert any(r["other_task_id"] == 2 for r in task_1["relations"])

    def test_list_shows_relation_flag(self, runner):
        lines = invoke(runner, "ls").output.splitlines()
        task_1_line = next(line for line in lines if line.strip().startswith("1 ("))
        assert "L" in task_1_line
