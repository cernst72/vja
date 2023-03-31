# Features

<!-- TOC -->
* [Features](#features)
  * [Create Task](#create-task)
    * [Clone](#clone)
  * [List tasks](#list-tasks)
    * [Urgency](#urgency)
    * [Filter](#filter)
    * [Sort](#sort)
    * [Select](#select)
  * [Show single task by id](#show-single-task-by-id)
  * [Modify tasks](#modify-tasks)
    * [Defer task](#defer-task)
    * [Reminders](#reminders)
    * [Batch editing](#batch-editing)
  * [Open Vikunja in browser](#open-vikunja-in-browser)
  * [Manage lists, namespaces, labels, buckets](#manage-lists-namespaces-labels-buckets)
    * [Manage namespaces](#manage-namespaces)
    * [Manage lists (projects)](#manage-lists-projects)
    * [Manage kanban buckets](#manage-kanban-buckets)
    * [Manage labels](#manage-labels)
  * [Output format](#output-format)
  * [Terminate session](#terminate-session)
<!-- TOC -->

## Create Task

`vja add <Tasktitle>` allows to quickly add a new task to the default list. Several options exist to provide more
context:

```shell
vja add Getting things done --note="find out how" -priority=3 --favorite=True --due="tomorrow at 11:00" --reminder --tag=@work
```

or more concise

```shell
vja add One more task -l 1 -p 4 -t "Label1" -n "my note" -d "23:00" -f True
```

See

```shell
vja add --help
```

for more.

### Clone

Another option to create a new task is cloning an existing task

```shell
vja clone 1 Clone a new task
```

See

```shell
vja clone --help
```

## List tasks

List all active tasks

```shell
vja ls
vja ls --json
```

### Urgency

By default, tasks are sorted (amongst others) by their urgency, which is displayed in the last column. Urgency is
calculated by regarding due_date, priority and is_favorite of the task, as well as the occurence of keywords in the list
title or the label titles. The weights of each factor and the keywords can be specified in the configuration file ~
/.vjacli/vja.rc. See Configuration section in [Readme.md](Readme.md). See [.vjacli/vja.rc](.vjacli/vja.rc) for an
example.

### Filter

The displayed tasks may be filtered by several arguments like list id or title, namespace and label

```shell
vja ls --label=@work
vja ls --title=ask
vja ls --priority="gt 3"
vja ls --priority="eq 5"
vja ls --due-date="before today"
vja ls --due-date="ge in 0 days" --due-date="before 5 days"
vja ls -u   # show Tasks with minimum urgency
vja ls --urgency=8 # show quite urgent tasks
```

In addition to these shortcut filters, more general filtering can be done by `--filter=<field_name> <operator> <value>`:

```shell
vja ls --filter="priority gt 2"
vja ls --filter="title contains clean up"
vja ls --filter="labels contains @work"
vja ls --filter="created after 2 days ago"
vja ls --filter="due_date before today in 7 days"
```

See `vja ls --help` for more.

### Sort

Sorting of tasks can be achieved by setting the `--sort` option.

```shell
vja ls --sort=id
vja ls --sort=-id # reverse
```

Sort criteria can be combined. The default sort order of vja is the same as

```shell
vja ls --sort='done, -urgency, due_date, -priority, tasklist.title, title'
```

See `vja ls --help` for more.

### Select

Columns may be selected and formatted in .vjarc and activated via `--custom-format`.
See [Output format](#output-format)

See `vja ls --help` for more.

## Show single task by id

```shell
vja show 1
vja show 1 --json
vja show 1 2 3

```

## Modify tasks

```shell
vja edit 1 --title="new title" --due-date="friday" --priority=1
```

Set new due_date and set reminder=due_date

```shell
vja edit 1 --due="in 4 days at 15:00" -r
```

Toggle tag (=label). Use with --force to create new label:

```shell
vja edit 1 -t @work
```

Mark as done

```shell
vja edit 1 --done="true"
vja check 1 # Shortcut to toggle the done flag of task 1
```

### Defer task

There is a shortcut for setting a delay on a task by giving a timedelta expression.

```shell
vja defer 1 1d
vja defer --help
```

This command moves the due_date and the first reminder ahead in time.

### Reminders

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

### Batch editing

Multiple edits and defers are possible by giving more task ids

```shell
vja edit 1 5 8 --due="next monday 14:00"
vja defer 1 2 3 1d
```

See

```shell
vja edit --help
```

for more.

## Open Vikunja in browser

Open starting page

```shell
vja open
```

Open task 42 in browser

```shell
vja open 42
```

## Manage lists, namespaces, labels, buckets

### Manage namespaces

```shell
vja namespace ls
```

### Manage lists (projects)

```shell
vja list add New List
```

```shell
vja list add -n 2 Create list in namespace with index 2
```

```shell
vja list ls
```

```shell
vja list show 1
```

### Manage kanban buckets

```shell
vja bucket ls --list-id=1
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

See [example](https://gitlab.com/ce72/vja/-/blob/main/.vjacli/vja.rc). This can be activated e.g.
with `vja ls --custom-format=ids_only`.

Be careful: The format string may contain arbitrary code, which gets executed at runtime (python eval()).
Do not use `--custom-format` if you feel uncomfortable with that.

## Terminate session

You may remove your traces by logging out. This will remove the local access token so that during subsequent execution
vja will prompt you again.

```shell
vja logout
```

