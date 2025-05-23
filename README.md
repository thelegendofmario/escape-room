# Escape Room in Slack

## What is This?
an escape room! (a simple 3 puzzles)

## How do I Play?
simply add this bot to a channel or group DM and type 'START' to start!

## Running it Locally
(if you really want to lol)

this was developed with the awesome `uv` tool by [astral.sh](https://astral.sh/).
If you don't already have it, I suggest you get it [here](https://github.com/astral-sh/uv).

regardless, clone the repo, then run `pip install .` or you can just run it without intalling with `uv run escape-room`

then, run it with `escape-room`.

### Possible Arguments
The only possible arguments are `--http` and `--port [number]`.

`--http` is a flag, use it if you don't want to use socket mode.
if you use `--http`, you have to specify a port number with `--port [number]`.