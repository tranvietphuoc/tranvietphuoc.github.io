#! /bin/bash

# clean html files in posts folder and index.html file
rm index.html
rm ./posts/*.html
rm ./tags/*.html

if [ ! -d ".venv" ]; then
    poetry update
else
    poetry run python app.py
fi

