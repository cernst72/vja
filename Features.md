# Features

## Create Tasks
`vja add <Tasktitle>` allows to quickly add a new task to the default list. Several options exist to provide more context:

```shell
vja add Make things work --note="find out how" -priority=3 --favorite=True --due="tomorrow at 11:00" --reminder --tag=@work
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

## List tasks

List all active tasks

```shell
vja ls
vja ls --json
```

Some filters exist like id or title of list, namespace and label

```shell
vja ls --label="@work"
vja ls --title="ask"
vja ls -u   # show Tasks with minimum urgency
vja ls -u 6 # show quite urgent tasks

```

See `vja ls --help` for more.

### Show task by id

```shell
vja show 1
vja show 1 --json
vja show 1 2 3

```

Display single task with full information:

```shell
vja -v show 1
```

## Modify task

```shell
vja edit 1 --title="new title" --due="friday" --prio=1
```

```shell
vja edit 1 --done="true"
vja check 1 # Shortcut to toggle the done flag of task 1
```

Multiple edits are possible by giving more task ids

```shell
vja edit 1 5 8 --due="next monday at 14:00"
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

## Manage lists, namespaces, labels

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

## Terminate session

You may remove your traces by logging out. This will remove the local access token so that during subsequent execution
vja will prompt you again.

```shell
vja logout
```

