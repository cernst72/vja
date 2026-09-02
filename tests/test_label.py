import re

from tests.conftest import invoke


class TestLabel:
    def test_label_ls(self, runner):
        res = invoke(runner, "label ls")
        assert re.search(r"my_tag", res.output)

    def test_label_ls_custom_format(self, runner):
        res = invoke(runner, "label ls --custom-format=ids_only")
        lines = [line for line in res.output.splitlines() if line]
        assert len(lines) > 0
        for line in lines:
            assert re.match(r"^\d+$", line), line
