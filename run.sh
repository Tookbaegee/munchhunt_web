#!/bin/bash
if [[ ! -d migrations ]]; then
    echo "Please run setup.sh before continuing."
else
    source venv/bin/activate
    flask run
fi