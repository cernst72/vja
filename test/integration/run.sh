#!/bin/bash
set -euo pipefail

export VJA_CONFIGDIR=.vjatest

run-test () {
  set -x
  vja --version
  vja --help
  vja -u demo -p demo ls
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
  vja edit 1 --prio=0 --note="" --due="" --favorite=False --reminder="" --title="empty title" --completed=True
  vja edit 2 --prio=1 --note="modified note" --due="4.2" --reminder="tomorrow"
  vja show 1
  vja show 1 --json
  vja show 1 --jsonvja
  vja list show 1 --json
  vja bucket ls -l 1
  vja label ls --json
  vja namespace ls
  vja -v logout
  vja -v -u demo -p demo ls
  vja -v list ls
  vja -v edit 1 --prio=5 --favorite=True
  vja -v show 1
  vja -v ls
}

start-vikunja () {
  host=$1
  compose_file=$2
  echo "start vikunja service"
  set -x
  docker-compose -f "$compose_file" up -d
  timeout 30 bash -c "while [[ \"\$(curl -s -o /dev/null -w ''%{http_code}'' http://$host:3456/api/v1/info)\" != \"200\" ]]; do sleep 1; done" || false
  curl "http://$host:3456/api/v1/info"
  docker-compose -f "$compose_file" exec -T api /app/vikunja/vikunja user create -u demo -p demo -e demo@demo.demo
  exit 0
}

stop-vikunja () {
  echo "stop vikunja service"
  docker-compose -f "$1" down
  exit 0
}

setup-test () {
  host=$1
  mkdir -p $VJA_CONFIGDIR
  rm $VJA_CONFIGDIR/token.json 2> /dev/null || true
  cat > $VJA_CONFIGDIR/vja.rc << EOF
[application]
frontend_url=http://$host:8080/
api_url=http://$host:3456/api/v1
EOF
}

command="${1}"
host="${2:-localhost}"
compose_file="${3:-docker-compose.yml}"
[[ $command == 'start' ]] && start-vikunja "$host" "$compose_file"
[[ $command == 'stop' ]] && stop-vikunja "$compose_file"
setup-test "$host"
run-test


