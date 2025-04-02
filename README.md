# EmbedderTg

## Development

Some development dependecies used in this project are:

- [poetry](https://github.com/python-poetry/poetry)
- Any editor using [pyright](https://github.com/microsoft/pyright)

## Installation:

Use Linux with systemd. The script will install a new systemd script for user service manager, if you wish to install it system-wide, tweak `Makefile` as you see fit.

1. Create `.env` file:

```
BOT_TOKEN=<YOUR_BOT_TOKEN>
```

If you don't have a bot token, follow this part of the official tutorial: https://core.telegram.org/bots/tutorial#obtain-your-bot-token

2. Install

```sh
make install
```

(Alternative) 2. If you just want to run it without installing a systemd service:

```
poetry run python3 embeddertg
```
