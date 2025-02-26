# Features

<!-- TOC -->
* [Features](#features)
  * [Login](#login)
    * [API token](#api-token)
  * [Tasks](#tasks)
    * [Add Task](#add-task)
      * [Clone](#clone)
    * [List tasks](#list-tasks)
      * [Urgency](#urgency)
      * [Sort](#sort)
      * [Filter](#filter)
      * [Select](#select)
    * [Show single task](#show-single-task)
    * [Edit tasks](#edit-tasks)
      * [Defer task](#defer-task)
      * [Reminders](#reminders)
      * [Batch editing](#batch-editing)
  * [Open Vikunja in browser](#open-vikunja-in-browser)
  * [Manage projects, labels, buckets](#manage-projects-labels-buckets)
    * [Manage projects](#manage-projects)
    * [Manage kanban buckets](#manage-kanban-buckets)
    * [Manage labels](#manage-labels)
  * [Output format](#output-format)
    * [Example](#example)
  * [Terminate session](#terminate-session)
<!-- TOC -->

## Login

When no valid token file exists in `$HOME/.vjacli/` then vja will ask for username and password on first usage.
If Two-Factor Authentication is activated for your user then vja will prompt you for the one-time password additionally.
The resulting token will be stored in `$HOME/.vjacli/token.json`.

### API token

Alternatively you may create an API token with sufficient rights in Vikunja ("Settings -> API Tokens")
and save it to `$HOME/.vjacli/token.json`

```json
{
  "token": "YOUR-API-TOKEN"
}
```

The token permission must include at least Labels, Projects, Tasks, User as well as all required relations with all
operations, depending on what you want to use vja for.

## Tasks

All task related commands are supported in two variants:
`vja add`, `vja ls`, ...
as well as
`vja task add`, `vja task ls`, ... (and even `vja tasks...`).

### Add Task

`vja add <Tasktitle>` allows to quickly add a new task to the default project. Several options exist to provide more
context:

```shell
vja add Getting things done --note="find out how" -priority=3 --favorite --due="tomorrow at 11:00" --reminder --label=@work
```

or more concise

```shell
vja add One more task -o 1 -p 4 -l "Label1" -n "my note" -d "23:00" -f
```

See

```shell
vja add --help
```

for more.

#### Clone

Another option to create a new task is cloning an existing task

```shell
vja clone 1 Copy a task with this new title
```

See

```shell
vja clone --help
```

### List tasks

List all active tasks

```shell
vja ls
vja ls --json
```

You may limit the output by giving task ids

```shell
vja ls 10 13 14
```

#### Urgency

By default, tasks are sorted (amongst others) by their urgency, which is displayed in the last column. Urgency is
calculated by regarding due_date, priority and is_favorite of the task, as well as the occurrence of keywords in the
project title or the label titles. The weights of each factor and the keywords can be specified in the configuration
file `~/.vjacli/vja.rc`. See Configuration section in [README.md](README.md). See [`.vjacli/vja.rc`](.vjacli/vja.rc) for an
example.

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

The displayed tasks may be filtered by several arguments like project or title, base_project and label

```shell
vja ls --project=1
vja ls -o=projec # matches regex string
vja ls --base-project=myproject
vja ls -t=projec # matches regex string
vja ls --due-date="before today"
vja ls --due-date="ge in 0 days" --due-date="before 5 days"
vja ls --favorite=True
vja ls --label=@work
vja ls -l=work # matches regex string
vja ls --priority="gt 3"
vja ls --priority="eq 5"
vja ls --title=ask # matches regex string
vja ls -u   # show Tasks with minimum urgency of 3
vja ls --urgency=8 # show only quite urgent tasks
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

#### Select

Columns may be selected and formatted in `.vjarc` and activated via `--custom-format`.
See [Output format](#output-format)

See `vja ls --help` for more.

### Show single task

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

See

```shell
vja edit --help
```

for more.

#### Defer task

There is a shortcut for setting a delay on a task by giving a timedelta expression.

```shell
vja defer 1 1d
vja defer --help
```

This command moves the due_date and the first reminder ahead in time.

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

## Open Vikunja in browser

Open starting page

```shell
vja open
```

Open task 42 and 43 in browser

```shell
vja open 42 43
vja edit 42 43
```

## Manage projects, labels, buckets

There is only a very basic support for managing entities other than tasks. I believe it is better to use the frontend.

### Manage projects

Projects can be added and be shown, but not be modified:

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
Run with `--custom-format=<template-name>` to refer a format string in your `vja.rc`.

See [vja.rc](https://gitlab.com/ce72/vja/-/blob/main/.vjacli/vja.rc). This can be activated e.g.
with `vja ls --custom-format=ids_only`.

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

