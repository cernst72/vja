from tests.conftest import invoke
from tests.test_command_helpers import json_for_task_id


class TestRelation:
    def test_add_creates_relation_and_inverse(self, runner):
        res = invoke(runner, "relation add 1 subtask 3")
        assert res.exit_code == 0
        source = json_for_task_id(runner, 1)
        assert any(
            r["kind"] == "subtask" and r["other_task_id"] == 3
            for r in source["relations"]
        )
        target = json_for_task_id(runner, 3)
        assert any(
            r["kind"] == "parenttask" and r["other_task_id"] == 1
            for r in target["relations"]
        )

    def test_remove_removes_relation_and_inverse(self, runner):
        invoke(runner, "relation add 1 subtask 3")
        assert invoke(runner, "relation remove 1 subtask 3").exit_code == 0
        source = json_for_task_id(runner, 1)
        assert not any(
            r["kind"] == "subtask" and r["other_task_id"] == 3
            for r in source["relations"]
        )
        target = json_for_task_id(runner, 3)
        assert not any(
            r["kind"] == "parenttask" and r["other_task_id"] == 1
            for r in target["relations"]
        )

    def test_verbose_show_displays_relation(self, runner):
        res = invoke(runner, "relation add 1 subtask 2 -v")
        assert "Modified task 1 in project" in res.output
        assert "subtask" in res.output

    def test_invalid_kind_is_rejected(self, runner):
        invoke(runner, "relation add 1 bogus 2", expected_return_code=2)
