set dotenv-load

default:
    just run

init:
    poetry update

run:
    poetry run python3 embeddertg
