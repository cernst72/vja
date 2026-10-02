import asyncio
import json

import pytest

pytest.importorskip("mcp", reason="optional 'mcp' dependency not installed (install with: pip install \"vja[mcp]\")")

from vja import mcp_server


def _tool_names() -> set[str]:
    return {tool.name for tool in asyncio.run(mcp_server.mcp.list_tools())}


def _call_tool(name: str, arguments: dict):
    result = asyncio.run(mcp_server.mcp.call_tool(name, arguments))
    assert not result.is_error, result
    return json.loads(result.content[0].text)


class TestMcpServer:
    def test_expected_tools_are_registered(self):
        names = _tool_names()
        expected = {
            "get_current_user",
            "list_projects",
            "list_labels",
            "list_tasks",
            "get_task",
            "add_task",
            "edit_task",
            "toggle_task_done",
            "defer_task",
            "clone_task",
        }
        assert expected <= names

    def test_delete_tool_is_not_exposed(self):
        assert "delete_task" not in _tool_names()

    def test_get_task_returns_baseline_task(self):
        task = _call_tool("get_task", {"task_id": 1})
        assert task["id"] == 1
        assert task["title"].startswith("At least one task")
        assert task["project"]["title"] == "test-project"
        assert any(label["title"] == "my_tag" for label in task["label_objects"])
