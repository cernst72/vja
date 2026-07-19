import re

from tests.conftest import invoke


class TestLabel:
    def test_label_ls(self, runner):
        res = invoke(runner, "label ls")
        assert re.search(r"my_tag", res.output)

    def test_label_ls_custom_format(self, runner):
        res = invoke(runner, "label ls --custom-format=ids_only")
        for line in res.output:
            assert re.match(r"^\d*$", line)
