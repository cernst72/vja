import re

from tests.conftest import invoke


class TestBucket:
    def test_bucket_ls(self, runner):
        res = invoke(runner, "bucket ls --project-id=Inbox")
        assert re.search(r"To-Do|Backlog", res.output)

    def test_bucket_ls_custom_format(self, runner):
        res = invoke(runner, "bucket ls --project-id=1 --custom-format=ids_only")
        for line in res.output:
            assert re.match(r"^\d*$", line)
