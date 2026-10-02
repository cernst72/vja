# Features

This is the command reference for `vja`. For installation and configuration, see
[README.md](README.md). Most examples use the short command form (`vja add`, `vja ls`, ...); every
command also accepts `--help`, and the [Appendix](#appendix) shows some handy shell aliases.

<!-- TOC -->
* [Features](#features)
  * [Login](#login)
    * [API token](#api-token)
  * [Tasks](#tasks)
    * [Add a task](#add-a-task)
      * [Clone](#clone)
    * [List tasks](#list-tasks)
      * [Urgency](#urgency)
      * [Sort](#sort)
      * [Filter](#filter)
      * [Select columns](#select-columns)
    * [Show a single task](#show-a-single-task)
    * [Edit tasks](#edit-tasks)
      * [Defer a task](#defer-a-task)
      * [Reminders](#reminders)
      * [Batch editing](#batch-editing)
    * [Delete a task](#delete-a-task)
    * [Task relations](#task-relations)
  * [Open Vikunja in browser](#open-vikunja-in-browser)
  * [Manage projects, labels, buckets](#manage-projects-labels-buckets)
    * [Manage projects](#manage-projects)
    * [Manage kanban buckets](#manage-kanban-buckets)
    * [Manage labels](#manage-labels)
  * [Output format](#output-format)
    * [Example](#example)
  * [Terminate session](#terminate-session)
  * [MCP server (use vja from AI agents)](#mcp-server-use-vja-from-ai-agents)
* [Appendix](#appendix)
<!-- TOC -->

## Login

When no valid token file exists next to your config file in the [configuration path](README.md#configuration) then vja will ask for username and password on first usage.
If Two-Factor Authentication is activated for your user then vja will prompt you for the one-time password additionally.
The resulting token will be stored in a file named `token.json` next to your config file.

### API token

Alternatively you may create an API token with sufficient rights in Vikunja ("Settings → API Tokens")
and save it to a file named `token.json` next to your configuration (e.g. `$HOME/.config/vja/config.rc`, see [README.md](README.md#configuration)).

```json
{
  "token": "YOUR-API-TOKEN"
}
```

The token permission must include at least Labels, Projects, Tasks, User as well as all required relations with all
operations, depending on what you want to use vja for.

## Tasks

All task-related commands come in two equivalent forms: the short form `vja add`, `vja ls`, ... and
the explicit form `vja task add`, `vja task ls`, ... (`vja tasks ...` works too). The examples below
use the short form.

### Add a task

`vja add <title>` quickly adds a new task to the default project. Several options add more context:

```shell
vja add Getting things done --note="find out how" --priority=3 --favorite --due="tomorrow at 11:00" --reminder --label=@work
```

or more concise

```shell
vja add One more task -o 1 -p 4 -l "Label1" -n "my note" -d "23:00" -f
```

See `vja add --help` for the full list of options.

#### Clone

You can also create a task by cloning an existing one:

```shell
vja clone 1 Copy a task with this new title
```

See `vja clone --help` for more.

### List tasks

List all active tasks:

```shell
vja ls
vja ls --json
```

Limit the output to specific task ids:

```shell
vja ls 10 13 14
```

#### Urgency

By default, tasks are sorted (amongst others) by their urgency, which is displayed in the last column. Urgency is
calculated by regarding due_date, priority and is_favorite of the task, as well as the occurrence of keywords in the
project title or the label titles. The weights of each factor and the keywords can be specified in your configuration
file (`config.rc`). See the Configuration section in [README.md](README.md#configuration).

#### Sort

Sorting of tasks can be achieved by setting the `--sort` option.

```shell
vja ls --sort=id
vja ls --sort=-id # reverse
```

Sort criteria can be combined. The default sort order of vja is the same as

```shell
vja ls --sort='done, -urgency, due_date, -priority, project.title, title'
```

See `vja ls --help` for more.

#### Filter

The displayed tasks may be filtered by several shortcut options, for example by project, base
project, label, title, due date, favorite, priority or urgency:

```shell
vja ls --project=1               # -o, by project id or title-regex
vja ls -o=projec                 # matches the project title as a regex
vja ls --base-project=myproject  # -t, filter by an ancestor (base) project
vja ls --label=@work             # -l, by label id or title-regex
vja ls -l=work                   # matches the label title as a regex
vja ls --title=ask               # -i, matches the task title as a regex
vja ls --due-date="before today"
vja ls --due-date="ge in 0 days" --due-date="before 5 days"
vja ls --favorite=True
vja ls --priority="gt 3"
vja ls --priority="eq 5"
vja ls -u                        # tasks with a minimum urgency of 3
vja ls --urgency=8               # only quite urgent tasks
```

In addition to these shortcut filters, more general filtering can be done by `--filter=<field_name> <operator> <value>`:

```shell
vja ls --filter="created after 2 days ago"
vja ls --filter="due_date before today in 7 days"
vja ls --filter="labels contains @work"
vja ls --filter="labels ne @work"
vja ls --filter="priority gt 2"
vja ls --filter="title contains clean up"
```

All filters can be combined:

```shell
vja ls --filter="labels ne @work" --project=1 --urgent
```

See `vja ls --help` for more.

#### Select columns

Columns may be selected and formatted in the `[output]` section of your `config.rc` and activated via
`--custom-format`. See [Output format](#output-format) for details.

### Show a single task

```shell
vja show 1
vja show 1 --json
vja show 1 2 3
```

### Edit tasks

```shell
vja edit 1 --title="new title" --due-date="friday" --priority=1 --star
vja edit 1 --no-star
```

Set new due_date and set reminder=due_date

```shell
vja edit 1 --due="in 4 days at 15:00" -r
```

Toggle label. Use with --force to create new label:

```shell
vja edit 1 -l @work
```

Note that `-l` in `vja edit` only allows to toggle a single label, while `vja add -l ... -l ...` allows to add a task
with multiple labels.

Mark as done

```shell
vja edit 1 --done="true"
vja check 1 # Shortcut to toggle the done flag of task 1
```

Called without any options, `vja edit <id>` opens the task in the browser (like `vja open <id>`).

See `vja edit --help` for the full list of options.

#### Defer a task

`vja defer` is a shortcut for pushing a task back by a timedelta expression. It moves the due_date and
the first reminder ahead in time.

```shell
vja defer 1 1d
vja defer --help
```

#### Reminders

vja manages only the first reminder of the task. That is the earliest reminder on the server.

Set reminder to an absolute time

```shell
vja edit 1 -r "next sunday at 11:00"
vja edit 1 --reminder="in 3 days at 11:00"
```

Set reminder equal to due date

```shell
vja edit 1 -r
vja edit 1 --reminder
```

Set reminder relative to due date (only due date is supported by vja for relative reminders)

```shell
vja edit --reminder="1h before due_date"
vja edit -r "10m before due"
```

Remove the earliest reminder

```shell
vja edit 1 -r ""
vja edit 1 --reminder=""
```

The same goes for `vja add`.

#### Batch editing

Multiple edits and defers are possible by giving more task ids. Take care though, there is no confirmation request.

```shell
vja edit 1 5 8 --due="next monday 14:00"
vja defer 1 2 3 1d
```

### Delete a task

```shell
vja delete 1
vja delete 1 2 3
```

### Task relations

Tasks may be linked to each other, for example as subtask, blocking or related. Existing relations are
shown in the details of a task and flagged with an `L` in the task list.

```shell
vja show 1      # relations are listed in the output
vja ls          # tasks having relations are marked with an "L" flag
```

Relations are created and removed with `vja relation add` and `vja relation remove` (also `rm` or
`delete`). The kind of relation is given as the middle argument. The inverse relation (for example
`parenttask` for a `subtask`) is maintained automatically by the server.

```shell
vja relation add 1 subtask 2       # task 2 becomes a subtask of task 1
vja relation remove 1 subtask 2
vja relation add 1 blocking 3 -v   # -v shows the resulting task
```

The available kinds are `subtask`, `parenttask`, `related`, `duplicateof`, `duplicates`, `blocking`,
`blocked`, `precedes`, `follows`, `copiedfrom` and `copiedto`.

```shell
vja relation --help
```

## Open Vikunja in browser

Open starting page

```shell
vja open
```

Open task 42 and 43 in browser

```shell
vja open 42 43
```

## Manage projects, labels, buckets

Support for entities other than tasks is intentionally basic; for anything more involved the web
frontend is usually the better choice.

### Manage projects

Projects can be added and shown, but not modified:

```shell
vja project add New Project
```

```shell
vja project add Create project in parent project by id -o 2
vja project add Create project in parent project by title -o my-parent
```

```shell
vja project ls
```

```shell
vja project show 1
```

Open in webbrowser:

```shell
vja project open 1
```

### Manage kanban buckets

```shell
vja bucket add Doing --project=1
```

```shell
vja bucket ls --project-id=1
```

### Manage labels

```shell
vja label add Next action
```

```shell
vja label ls
```

## Output format

You may specify custom list output formats (selecting and formatting columns).
Define them in the `[output]` section of your `config.rc` and run with
`--custom-format=<template-name>` to reference one.

See the example [config.rc](https://gitlab.com/ce72/vja/-/blob/main/.config/vja/config.rc). A format can be
activated e.g. with `vja ls --custom-format=ids_only`.

Be careful: The format string may contain arbitrary code, which gets executed at runtime (python eval()).
Do not use `--custom-format` if you feel uncomfortable with that.

### Example

The following command generates a script which may be executed against another instance
to re-import your active Vikunja tasks (only a few attributes):

```shell
vja ls --sort=id --custom-format=reimport > import.sh
```

(`export PYTHONIOENCODING=utf8` if you have encoding issues)

## Terminate session

You may remove your traces by logging out. This will remove the local access token so that at a subsequent execution
vja will prompt you again.

```shell
vja logout
```

## MCP server (use vja from AI agents)

`vja` ships an [MCP](https://modelcontextprotocol.io) server that exposes task
operations as tools for AI agents (Claude, Kiro, Cursor, ...). It shares the
same service layer as the CLI, so the tools behave exactly like the matching
`vja task ...` commands.

Install the optional `mcp` dependency and use the same configuration as the CLI
(a `config.rc` with a valid token, see [README.md](README.md#configuration)):

```shell
pipx install "vja[mcp]"   # or: pip install "vja[mcp]"
```

The server is started over stdio (the transport MCP clients expect for a local
server) via the `vja-mcp` entry point. Most clients start it for you from a JSON
config using the shared `mcpServers` schema:

```json
{
  "mcpServers": {
    "vja": {
      "command": "vja-mcp"
    }
  }
}
```

Only set `VJA_CONFIGDIR` when your config lives outside the default locations.
If `vja-mcp` is not on `PATH`, point `command` at the executable in the
environment you installed it into (e.g. `.../venv/bin/vja-mcp`, or
`...\Scripts\vja-mcp.exe` on Windows).

The exposed tools mirror the CLI:

- read: `get_current_user`, `list_projects`, `list_labels`, `list_tasks`, `get_task`
- write: `add_task`, `edit_task`, `toggle_task_done`, `defer_task`, `clone_task`

Tools return the same application JSON as `vja ls --json`. For agent-specific
guidance (registration details, handling large tool output, date filters) see
[AGENTS.md](https://gitlab.com/ce72/vja/-/blob/main/AGENTS.md).

# Appendix

Some shell aliases that show how these commands fit into a daily workflow:

```shell
vadd='vja add -v -o Next --priority=1 --reminder --due-date="tomorrow 08:00"'
vadda='vja add -v -o Next --priority=1 --reminder --due-date="tomorrow 08:00" --label="@arbeit"'
vaddc='vja add -v -o Next --priority=1 --reminder --due-date="tomorrow 08:00" --label="@computer"'
vaddh='vja add -v -o Next --priority=1 --reminder --due-date="tomorrow 08:00" --label="@zuhause"'
vaddu='vja add -v -o Next --priority=1 --reminder --due-date="tomorrow 08:00" --label="@unterwegs"'
vaddz=vaddh
vcheck='vja check -v'
vdate='vja edit -v -d'
vdefer='vja defer -v'
vedit='vja edit -v'
vla='vja ls -v --filter="labels contains @arbeit"'
vlcreated='vja ls -v --filter="created after last week" --custom-format=created --sort=created'
vldone='vja ls -v --filter="done eq True" --filter="updated after last week" --custom-format=updated --sort=updated --all'
vldue='vja ls -v --sort="due_date, -urgency"'
vlfrei='vja ls -v --filter="labels ne @arbeit" --filter="labels ne @arbeit,R"'
vlnow='vja ls -v --sort="due_date, -urgency" -u6'
vlu='vja ls -v -u'
vlupdated='vja ls -v --filter="updated after last week" --custom-format=updated --sort=updated --all'
vluu='vja ls -v -u 6'
vopen='vja open'
```


