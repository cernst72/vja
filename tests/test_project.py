import re

from tests.conftest import invoke


class TestProject:
    def test_project_ls(self, runner):
        res = invoke(runner, "project ls")
        assert re.search(r"test-project", res.output)

    def test_project_show_by_id(self, runner):
        res = invoke(runner, "project show 1")
        assert len(res.output) > 0

    def test_project_show_by_title(self, runner):
        res = invoke(runner, "project show test-project")
        assert len(res.output) > 0

    def test_project_ls_custom_format(self, runner):
        res = invoke(runner, "project ls --custom-format=ids_only")
        lines = [line for line in res.output.splitlines() if line]
        assert len(lines) > 0
        for line in lines:
            assert re.match(r"^-?\d+$", line), line
