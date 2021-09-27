#! /bin/bash

if [ ! -d ".venv" ]; then
    poetry update
else
    poetry run python app.py
fi

