#!/bin/bash
set -euo pipefail

export VJA_CONFIGDIR=.vjatest

run-test () {
  set -x
  vja --version
  vja --help
  vja -u demo -p demo ls
  vja namespace ls
  vja list add List from $(date)
  vja -v list ls
  vja label ls
  vja add Task from $(date)
  vja add Task from $(date)
  vja ls
  vja -v show 1
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


