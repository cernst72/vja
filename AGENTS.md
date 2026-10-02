# AGENTS.md

Guidance for AI coding agents and MCP-capable tools working in this repository.
This file uses the vendor-neutral [AGENTS.md](https://agents.md) convention so
that any agent (Claude, Cursor, Kiro, Gemini, etc.) can discover it. Tool
specific files (e.g. `CLAUDE.md`, `.kiro/steering/`) point back here.

## vja MCP server

`vja` ships an MCP server (`vja/mcp_server.py`) that exposes Vikunja task
operations as tools, parallel to the CLI. Both share the same service layer, so
the MCP tools behave exactly like the corresponding `vja task ...` commands.

### Install

The MCP server needs the optional `mcp` dependency:

```
pip install "vja[mcp]"
```

`vja` must be configured the same way as for CLI use (a `config.rc` with a valid
token; see the README). The server reads the same configuration and looks for it
in the same locations as the CLI, in order:

1. `$VJA_CONFIGDIR/config.rc`
2. `$XDG_CONFIG_HOME/vja/config.rc`
3. `$HOME/.config/vja/config.rc`
4. legacy `$HOME/.vjacli/vja.rc`

`VJA_CONFIGDIR` is optional. If your config lives in one of the default
locations you do not need to set it.

### Register the server

MCP clients read a JSON config with a shared `mcpServers` schema. A
project-level `.mcp.json` lives in the repository root and is picked up by tools
that support it (e.g. Claude Code):

```json
{
  "mcpServers": {
    "vja": {
      "command": "vja-mcp"
    }
  }
}
```

Only set `VJA_CONFIGDIR` when your config is in a non-default directory:

```json
{
  "mcpServers": {
    "vja": {
      "command": "vja-mcp",
      "env": {
        "VJA_CONFIGDIR": "/absolute/path/to/config/dir"
      }
    }
  }
}
```

If `vja-mcp` is not on `PATH`, use the interpreter from the environment it was
installed into, e.g. `"command": "/path/to/venv/bin/vja-mcp"` (or
`...\\Scripts\\vja-mcp.exe` on Windows).

> Note: some clients keep their MCP config elsewhere and use additional keys.
> For example Kiro reads `.kiro/settings/mcp.json` and supports `disabled` and
> `autoApprove`. Those keys are client-specific extensions of the same schema.

### Available tools

Read:

- `get_current_user`
- `list_projects`
- `list_labels`
- `list_tasks` — filter by project, label, title, priority, due, or free-form
  `general_filter` entries; optional sort string
- `get_task`

Write:

- `add_task`
- `edit_task` — only the fields you pass are changed; `label`/`assignee` toggle
- `toggle_task_done`
- `defer_task`
- `clone_task`

Tools return the vja application JSON (the same shape as `vja task ls --jsonvja`).
Domain errors are surfaced as tool errors with a readable message.

## Practical notes (agent usage)

### Large tool output

- `list_tasks` returns the full application JSON per task, including nested
  `project` and `views`. An unfiltered list can be very large and may exceed a
  client's tool-output limit; even a single-day filter can still be sizeable.
  Some clients spill the full result to a temporary file and only show a preview.
- Such a spilled file is a stream of concatenated JSON objects, **not** a single
  JSON array. `json.load` fails with "Extra data"; parse it by looping with
  `json.JSONDecoder().raw_decode` over the whitespace-separated objects.
- Prefer narrowing at the source: tighter `general_filter`, `project`/`label`,
  or a specific `title` regex keeps output small and avoids the file round-trip.
### Date filters (`due`)

- The `due` argument expects an `<operator> <value>` string, like the other
  operator-based filters. A bare value such as `due=tomorrow` fails; use an
  explicit operator, e.g. `due="eq tomorrow"`, `due="before tomorrow 23:59"`,
  or `due="after today 23:59"`.
- Natural-language date values work (`tomorrow`, `today 18:00`, `in 3 days`),
  but only together with an operator.
- `due="eq tomorrow"` is the cleanest way to get exactly one day. Range-style
  filters like `before`/`after` also include everything earlier/later, so
  `before tomorrow 23:59` returns overdue tasks too; combine two `general_filter`
  entries (`due after today 23:59` and `due before tomorrow 23:59`) for a strict
  single-day slice.
