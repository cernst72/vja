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
