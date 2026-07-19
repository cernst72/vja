import re

from tests.conftest import invoke


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
