# (Planned) Features of vja

## Create Tasks

```shell
vja add Learn using vja
```

```shell
vja add -l 2 Create task in list with index 2
```

```shell
vja add Create another task
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
vja list -n 2 Create list in namespace with index 2
```

## Manage labels

```shell
vja label ls
```

