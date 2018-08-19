#!/bin/bash
set -e
set -x

docker run -it --rm $_DOCKER_ARGS shitpostd:latest $@
