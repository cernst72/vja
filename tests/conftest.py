import json
import logging
import os
import subprocess
import sys

import click
import pytest
from click.testing import CliRunner

from vja.cli import cli

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


@pytest.fixture(name="runner", scope="session")
def setup_runner():
    return CliRunner()


def invoke(runner, command, expected_return_code=0, user_input=None, catch_exceptions=False):
    if isinstance(command, str):
        command = command.split()
    res = runner.invoke(cli, command, input=user_input, catch_exceptions=catch_exceptions)
    sys.stdout.write(res.output)
    if res.stderr_bytes:
        sys.stdout.write(res.stderr)
    if res.exception:
        logging.warning(res.exception)
    if expected_return_code is not None:
        assert res.exit_code == expected_return_code, res
    return res


def invoke_error(runner, command, expected_return_code=1, user_input=None):
    """Invoke a command that is expected to fail.

    Catches exceptions raised by the command so the resulting exit code can be
    asserted, instead of letting the exception propagate out of the test.
    """
    return invoke(
        runner,
        command,
        expected_return_code=expected_return_code,
        user_input=user_input,
        catch_exceptions=True,
    )


def _login_as_test_user():
    run_vja("logout")
    run_vja("--username=test --password=test user show")


# Defined baseline state of the shared core tasks (ids 1, 2, 3). Both the
# initial setup (_create_project_and_task) and the optional per-test reset
# (_reset_core_task) derive the task fields from this single source of truth
# to avoid duplication and drift. Insertion order determines the task ids.
_CORE_TASK_BASELINE = {
    1: {
        "title": "At least one task",
        "priority": 5,
        "due": "today",
        "favorite": True,
        "labels": ["my_tag"],
        "project": "test-project",
        "relations": [("related", 2)],
    },
    2: {
        "title": "Task in subproject",
        "priority": 0,
        "due": "",
        "favorite": False,
        "labels": [],
        "project": "grand-child",
        "relations": [("related", 1)],
    },
    3: {
        "title": "A task without a label",
        "priority": 0,
        "due": "",
        "favorite": False,
        "labels": [],
        "project": "Inbox",
        "relations": [],
    },
}


def _add_task_args_from_baseline(baseline):
    args = ["task", "add", baseline["title"], "--force-create", f"--priority={baseline['priority']}"]
    if baseline["due"]:
        args.append(f"--due-date={baseline['due']}")
    for label in baseline["labels"]:
        args.append(f"--label={label}")
    if baseline["favorite"]:
        args.append("--favorite")
    if baseline["project"] != "Inbox":
        args.append(f"--project-id={baseline['project']}")
    return args


def _create_project_and_task():
    run_vja("project add test-project")
    run_vja("project add child --parent-project=test-project")
    run_vja("project add grand-child --parent-project=child")
    run_vja("bucket add --project=test-project Second bucket")

    for baseline in _CORE_TASK_BASELINE.values():
        run_vja(_add_task_args_from_baseline(baseline))

    # Relations are bidirectional; create each pair once (from the lower task id).
    run_vja("relation rm 1 related 2", 1)
    run_vja("relation rm 1 subtask 2", 1)
    run_vja("relation rm 1 subtask 3", 1)
    run_vja("relation add 1 related 2")
    run_vja("task ls")
    run_vja("task show 1")


def run_vja(command, expected_return_code=0):
    args = command.split() if isinstance(command, str) else list(command)
    result = subprocess.run(["vja", *args], capture_output=True, check=False)
    if result.returncode and expected_return_code != result.returncode:
        click.echo(f"!!! Non-zero result ({result.returncode}) from vja {command}")
        sys.stdout.write(result.stdout.decode("utf-8"))
        sys.stdout.write(result.stderr.decode("utf-8"))
        pytest.exit(f"vja {command} failed with exit code {result.returncode}", returncode=1)


def pytest_addoption(parser):
    parser.addoption(
        "--reset-core-tasks",
        action="store_true",
        default=False,
        help="Restore the shared core tasks (ids 1, 2, 3) to their baseline after each test. ",
    )


def pytest_configure(config):
    if "VJA_CONFIGDIR" not in os.environ:
        pytest.exit("!!! Precondition not met. You must set VJA_CONFIGDIR in environment variables !!!", returncode=1)


@pytest.fixture(scope="session", autouse=True)
def setup_test_data():
    _login_as_test_user()
    _create_project_and_task()


def _show_task_json(runner, task_id):
    res = invoke(runner, f"show {task_id} --jsonvja")
    return json.loads(res.output)


def _reset_core_task(runner, task_id, baseline):
    current = _show_task_json(runner, task_id)

    # Deterministic (absolute) fields.
    edit_args = [
        "edit",
        str(task_id),
        "-i",
        baseline["title"],
        f"--priority={baseline['priority']}",
        f"--due={baseline['due']}",
        f"--project-id={baseline['project']}",
        "--completed=False",
        "--star" if baseline["favorite"] else "--no-star",
        "--reminder=",
    ]
    invoke(runner, edit_args)

    # Labels are toggled by the CLI, so align current -> baseline explicitly.
    current_labels = {label["title"] for label in current.get("label_objects") or []}
    target_labels = set(baseline["labels"])
    for label in current_labels ^ target_labels:
        invoke(runner, ["edit", str(task_id), f"--label={label}", "--force-create"])

    # Assignees are toggled too; remove any that are set.
    for assignee in current.get("assignee_objects") or []:
        invoke(runner, ["edit", str(task_id), f"--assignee={assignee['username']}"])

    # Relations: remove everything that is not in the baseline, add what is missing.
    target_relations = set(baseline["relations"])
    current_relations = {(rel["kind"], rel["other_task_id"]) for rel in current.get("relations") or []}
    for kind, other in current_relations - target_relations:
        invoke(runner, f"relation remove {task_id} {kind} {other}", expected_return_code=None, catch_exceptions=True)
    for kind, other in target_relations - current_relations:
        invoke(runner, f"relation add {task_id} {kind} {other}", expected_return_code=None, catch_exceptions=True)


@pytest.fixture(autouse=True)
def reset_core_tasks(request, runner, setup_test_data):
    """Optionally restore the shared core tasks (ids 1, 2, 3) to their baseline after each test."""
    yield
    if not request.config.getoption("--reset-core-tasks"):
        return
    for task_id, baseline in _CORE_TASK_BASELINE.items():
        _reset_core_task(runner, task_id, baseline)
