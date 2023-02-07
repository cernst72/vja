# Features

## Create Tasks

```shell
vja add Just drop a task in any first favorite list
```

```shell
vja -v add "Another task" --list=1 --prio=2 --tag="Next Action" --note="my note" --due="next monday at 15:00" --favorite=True --reminder="friday 12:00"
```

```shell
vja add "One mor task task" -l 1 -p 4 -t "Label1" -n "my note" -d "23:00" -f True
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
vja ls --label="Next Action"
vja ls --title="ask"
```
See `vja ls --help` for more.

### Show task by id
```shell
vja show 1
vja show 1 --json
```

Display single task with full information:

```shell
vja -v show 1
```

## Modify task

```shell
vja edit 1 --title="new title" --due="friday" --favorite=True
```

```shell
vja edit 1 --done="true"
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

Edit task 42 in browser

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

You may remove your traces by logging out. This will remove the local access token so that the subsequent execution of
vja will prompt you again.

```shell
vja logout
```

