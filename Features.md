# (Planned) Features of vja

## Create Tasks

```shell
vja add Create a quick task in any first favorite list
```

```shell
vja -v add "Another task" --prio=2 --tag="Next Action" --note="my note" --due="next monday at 15:00" --favorite=True --reminder="friday 12:00"
```

```shell
vja add "One mor task task" --list=1 -p 4 -t "Label1" -n "my note" -d "23:00" -f True
```

## List tasks

List all active tasks

```shell
vja ls
```

Display single task:

```shell
vja show 1
```

Display single task with full information:

```shell
vja -v show 1
```

## Open Vikunja in browser

Open starting page

```shell
vja open
```

Open task 42 in browser

```shell
vja open 42
```

## Manage namespaces

```shell
vja namespace ls
```

## Manage lists (projects)

```shell
vja list ls
```

```shell
vja list add New List
```

```shell
vja list add -n 2 Create list in namespace with index 2
```

## Manage labels

```shell
vja label add Next action
```

```shell
vja label ls
```

