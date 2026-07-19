import re

from tests.conftest import invoke

ADD_SUCCESS_PATTERN = r".*Created task (\d+) in project .*"


class TestDeleteTask:
    def test_delete_task(self, runner):
        res = invoke(runner, "add task to delete --force --project=test-project")
        task_id = re.match(ADD_SUCCESS_PATTERN, res.output).group(1)

        res = invoke(runner, f"delete {task_id}")
        assert res.exit_code == 0
        assert f"Deleted task {task_id}" in res.output

        invoke(runner, f"show {task_id}", expected_return_code=1)

    def test_delete_multiple_tasks(self, runner):
        task_ids = []
        for _ in range(2):
            res = invoke(runner, "add batch delete test --force --project=test-project")
            task_ids.append(re.match(ADD_SUCCESS_PATTERN, res.output).group(1))

        res = invoke(runner, f"delete {task_ids[0]} {task_ids[1]}")
        assert res.exit_code == 0
        for task_id in task_ids:
            assert f"Deleted task {task_id}" in res.output

        for task_id in task_ids:
            invoke(runner, f"show {task_id}", expected_return_code=1)

    def test_delete_nonexistent_task(self, runner):
        invoke(runner, "delete 99999", expected_return_code=1)
