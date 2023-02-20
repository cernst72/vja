#!/bin/bash
set -euo pipefail

run-test () {
  set -x
  vja --version
  vja --help
  vja -u test -p test ls
  vja user show
  vja list add Work
  vja list add Home
  vja list ls
  vja list show 1
  vja label add Next Action
  vja label ls
  vja add "Look around" --prio=2 --tag="Next Action" --note="my note" --due="next monday at 15:00" --favorite=True --reminder="friday 12:00"
  vja add "Stay at home" -p 4 -t "Next Action" -n "my note" -d "23:00" -f True --list=2
  vja add Go home
  vja ls
  vja ls --list=1
  vja ls --list=Work
  vja ls --label="Next Action"
  vja ls --title="home"
  vja ls --sort="-due_date"
  vja ls --custom-format=ids_only
  vja edit 1 --prio=0 --note="" --due="" --favorite=False --reminder="" --title="empty title" --completed=True
  vja edit 2 --prio=1 --note="modified note" --due="4.2" --reminder="tomorrow"
  vja show 1
  vja show 1 --json
  vja show 1 --jsonvja
  vja toggle 1
  vja list show 1 --json
  vja bucket ls -l 1
  vja label ls
  vja namespace ls
  vja -v logout
  vja -v -u test -p test ls
  vja -v list ls
  vja -v edit 1 --prio=5 --favorite=True
  vja -v show 1
  vja -v ls
}

run-test


