import json
import logging
import re

import pytest

from tests.conftest import invoke
from vja.config import VjaConfiguration


class TestBasicOptions:
    def test_version(self, runner):
        res = invoke(runner, "--version")
        assert re.match(r".*version \d+\.\d+\.\d+", res.output), res.output

    def test_no_args_displays_help(self, runner):
        res = invoke(runner, "", None)
        assert "Usage: cli [OPTIONS] COMMAND [ARGS]..." in res.output
        assert res.output.count("\n") > 20

    def test_help_ls(self, runner):
        res = invoke(runner, "ls --help")
        assert "Usage: cli ls [OPTIONS]" in res.output
        assert "List tasks" in res.output
        assert res.output.count("\n") > 12

    def test_verbose_logging(self, runner, caplog):
        caplog.set_level(logging.DEBUG)
        invoke(runner, "-v ls")
        assert "Read config from" in caplog.text
        assert "Connecting to api_url" in caplog.text


class TestLoginLogout:
    def test_logout_login_given_password(self, runner, caplog):
        invoke(runner, "logout")
        assert "Logged out" in caplog.text
        invoke(runner, "-u test -p test user show")
        assert "Login successful" in caplog.text

    def test_logout_login_wrong_given_password(self, runner, caplog):
        invoke(runner, "logout")
        assert "Logged out" in caplog.text
        invoke(
            runner,
            "-u testxx -p testxx user show",
            expected_return_code=1,
            catch_exceptions=True,
        )
        assert "Wrong username or password." in caplog.text
        invoke(runner, "-u test -p test user show")
        assert "Login successful" in caplog.text

    def test_logout_login_password_from_stdin(self, runner, caplog):
        invoke(runner, "logout")
        assert "Logged out" in caplog.text
        invoke(runner, "user show", user_input="test\ntest\n")
        assert "Login successful" in caplog.text

    def test_logout_login_wrong_password_from_stdin(self, runner, caplog):
        invoke(runner, "logout")
        assert "Logged out" in caplog.text
        res = invoke(
            runner,
            "user show",
            user_input="testy\ntesty\n",
            expected_return_code=1,
            catch_exceptions=True,
        )
        assert "Wrong username or password." in res.output
        invoke(runner, "-u test -p test user show")
        assert "Login successful" in caplog.text

    def test_prompt_when_invalid_token(self, runner, caplog):
        self._invalidate_token()
        res = invoke(runner, "user show", user_input="test\ntest\n")
        assert "Username" in res.output
        assert "Password" in res.output
        assert "Login successful" in caplog.text

    def test_http_error(self, runner, caplog):
        res = invoke(
            runner,
            "show 9999",
            expected_return_code=1,
        )
        assert "HTTP-Error 404" in res.output

    @staticmethod
    def _invalidate_token():
        config = VjaConfiguration()
        with open(config.get_token_file(), "w", encoding="utf-8") as token_file:
            json.dump({"token": "slightly outdated..."}, token_file)
