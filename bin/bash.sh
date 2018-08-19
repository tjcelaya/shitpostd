#!/bin/bash
set -e
set -x
_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

_DOCKER_ARGS="-v $_DIR/..:/usr/src/shitpostd --env-file $_DIR/../.env"
env -i _DOCKER_ARGS="$_DOCKER_ARGS" $_DIR/run.sh bash
