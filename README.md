# shitpostd

Bot that shitposts in response to everything it sees. It ignores messages in threads so you can have an actual conversatio near it.

## Building

Link the desired Dockerfile to `./Dockerfile` (e.g. `ln -snf Dockerfile.amd64 Dockerfile` for most) and run `bin/build.sh`. This generates a docker image named `shitpostd:latest`.

## Developing

Lol, sure. `bin/bash.sh` runs a dev container with the project directory mounted as the work directory. `bin/python.sh` takes you straight to a python shell.

## Running

`bin/run.sh`

Needs the following environment variables in `.env`:

```
SLACK_OAUTH_ACCESS_TOKEN
SLACK_BOT_ACCESS_TOKEN
GIPHY_API_KEY
```
