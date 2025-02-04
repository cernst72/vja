#!/bin/bash
set -euo pipefail

run-test () {
  set -x
  vja --version
  vja --help
  vja -u test -p test ls
  vja user show
  vja project add Work
  vja project add Home
  vja project ls
  vja project show 1
  vja label add Next Action
  vja label ls
  vja add "Look around" --prio=2 --label="Next Action" --note="my note" --due="next monday at 15:00" --favorite --reminder="friday 12:00"
  vja add "Stay at home" -p 4 -l "Next Action" -n "my note" -d "23:00" -f True --project=2
  vja add Go home
  vja ls
  vja ls --project=1
  vja ls --project=Work
  vja ls --label="Next Action"
  vja ls --title="home"
  vja ls --sort="-due_date"
  vja ls --custom-format=ids_only
  vja edit 1 --prio=0 --note="" --due="" --no-favorite --reminder="" --title="empty title" --completed=True
  vja edit 2 --prio=1 --note="modified note" --due="4.2" --reminder="tomorrow"
  vja clone 1 new title of cloned task
  vja show 1
  vja show 1 --json
  vja show 1 --jsonvja
  vja toggle 1
  vja project show 1 --json
  vja label ls
  vja -v logout
  vja -v -u test -p test ls
  vja -v project ls
  vja -v edit 1 --prio=5 --favorite
  vja -v show 1
  vja -v ls
}

run-test


