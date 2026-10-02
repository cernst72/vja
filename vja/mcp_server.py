"""Model Context Protocol server for vja.

Exposes Vikunja task operations as MCP tools for agents such as Kiro. The server
runs parallel to the CLI and shares the same service layer (``Application`` ->
``CommandService`` / ``QueryService``); it does not shell out to the CLI.

Run it directly for a stdio transport (the transport MCP clients expect for a
local server)::

    vja-mcp

Requires the optional ``mcp`` dependency::

    pip install "vja[mcp]"
"""

import logging
from functools import wraps

from vja import VjaError
from vja.application import Application

try:
    from mcp.server.mcpserver import MCPServer
    from mcp.server.mcpserver.exceptions import ToolError
except ModuleNotFoundError as error:  # pragma: no cover - import guard
    raise SystemExit(
        "The MCP server requires the 'mcp' package (>=2). Install it with: pip install \"vja[mcp]\""
    ) from error

logger = logging.getLogger(__name__)

mcp = MCPServer("vja")

_application: Application | None = None


def _app() -> Application:
    """Lazily build the shared Application so a failing config does not crash tool discovery."""
    global _application
    if _application is None:
        _application = Application()
    return _application


def tool(func):
    """Register a function as an MCP tool, surfacing VjaError as a client-visible message."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except VjaError as error:
            raise ToolError(str(error)) from error

    return mcp.tool()(wrapper)


def _drop_none(**kwargs) -> dict:
    """Keep only the arguments the caller actually set, mirroring the CLI's arg handling."""
    return {key: value for key, value in kwargs.items() if value is not None}


# --- read tools ---------------------------------------------------------------


@tool
def get_current_user() -> dict:
    """Return the currently authenticated Vikunja user."""
    return _app().query_service.find_current_user().data_dict()


@tool
def list_projects() -> list[dict]:
    """List all projects the user can access."""
    return [project.data_dict() for project in _app().query_service.find_all_projects()]


@tool
def list_labels() -> list[dict]:
    """List all labels."""
    return [label.data_dict() for label in _app().query_service.find_all_labels()]


@tool
def list_tasks(
    include_completed: bool = False,
    sort: str | None = None,
    project: str | None = None,
    label: str | None = None,
    title: str | None = None,
    priority: str | None = None,
    due: str | None = None,
    general_filter: list[str] | None = None,
) -> list[dict]:
    """List tasks, optionally filtered and sorted.

    Filters that take an ``<operator> <value>`` string (priority, due) use operators
    like eq, ne, gt, lt, ge, le, before, after, contains. ``project`` and ``label``
    accept an id or a title regex. ``general_filter`` entries look like
    "field operator value" (e.g. "priority ge 2") and are combined with logical AND.
    """
    filter_args = _drop_none(
        project_filter=project,
        label_filter=label,
        title_filter=title,
        priority_filter=priority,
        due_date_filter=due,
        general_filter=tuple(general_filter) if general_filter else None,
    )
    tasks = _app().query_service.find_filtered_tasks(include_completed, sort, filter_args)
    return [task.data_dict() for task in tasks]


@tool
def get_task(task_id: int) -> dict:
    """Return the full details of a single task by its id."""
    return _app().query_service.find_task_by_id(task_id).data_dict()


# --- write tools --------------------------------------------------------------


@tool
def add_task(
    title: str,
    project: str | None = None,
    note: str | None = None,
    priority: int | None = None,
    due: str | None = None,
    start: str | None = None,
    end: str | None = None,
    favorite: bool | None = None,
    label: list[str] | None = None,
    assignee: list[str] | None = None,
    reminder: str | None = None,
    force_create: bool = False,
) -> dict:
    """Create a new task.

    Date fields (due, start, end) accept natural-language expressions like "tomorrow 18:00".
    ``project`` is an id or title; it defaults to the user's default project. Labels must
    already exist unless ``force_create`` is set. ``reminder`` supports absolute
    ("in 3 days at 18:00"), relative ("1h before due_date") or "due" expressions.
    """
    args = _drop_none(
        project_id=project,
        note=note,
        prio=priority,
        due=due,
        start=start,
        end=end,
        favorite=favorite,
        reminder=reminder,
    )
    args["label"] = tuple(label) if label else ()
    args["assignee"] = tuple(assignee) if assignee else ()
    args["force_create"] = force_create
    return _app().command_service.add_task(title, args).data_dict()


@tool
def edit_task(
    task_id: int,
    title: str | None = None,
    note: str | None = None,
    note_append: str | None = None,
    priority: int | None = None,
    project: str | None = None,
    due: str | None = None,
    start: str | None = None,
    end: str | None = None,
    favorite: bool | None = None,
    completed: bool | None = None,
    label: str | None = None,
    assignee: str | None = None,
    reminder: str | None = None,
    force_create: bool = False,
) -> dict:
    """Modify an existing task. Only the provided fields are changed.

    ``note_append`` adds a line to the existing description. ``label`` and ``assignee``
    are toggled: adding when absent, removing when already set. Labels must exist unless
    ``force_create`` is set.
    """
    args = _drop_none(
        title=title,
        note=note,
        note_append=note_append,
        prio=priority,
        project_id=project,
        due=due,
        start=start,
        end=end,
        favorite=favorite,
        completed=completed,
        label=label,
        assignee=assignee,
        reminder=reminder,
    )
    if force_create:
        args["force_create"] = True
    return _app().command_service.edit_task(task_id, args).data_dict()


@tool
def toggle_task_done(task_id: int) -> dict:
    """Toggle a task's done state (mark done if open, reopen if done)."""
    return _app().command_service.toggle_task_done(task_id).data_dict()


@tool
def defer_task(task_id: int, delay_by: str) -> dict:
    """Move a task's due date and reminders forward by a delay such as "2d" or "1h30m"."""
    return _app().command_service.defer_task(task_id, delay_by).data_dict()


@tool
def clone_task(task_id: int, title: str) -> dict:
    """Duplicate a task into the same project and give the copy a new title."""
    return _app().command_service.clone_task(task_id, title).data_dict()


def main() -> None:
    logging.basicConfig(level=logging.WARNING)
    mcp.run()


if __name__ == "__main__":
    main()
