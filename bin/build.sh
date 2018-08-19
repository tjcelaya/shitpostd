#!/bin/bash
set -e
set -x
_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

docker build -f $_DIR/../Dockerfile -t shitpostd:latest $_DIR/..
