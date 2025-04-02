[Unit]
Description=Telegram Media Embedder Bot

[Service]
ExecStart=poetry run python3 embeddertg
Restart=on-failure
RestartSec=1m
Type=idle
WorkingDirectory={{WORKING_DIRECTORY}}

[Install]
WantedBy=default.target
