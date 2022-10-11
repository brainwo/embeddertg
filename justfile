default:
    just run

init:
    poetry update

run:
    export $(cat secrets.env) && poetry run python3 embeddertg
