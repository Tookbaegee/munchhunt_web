#!/bin/bash
npm i
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
envsubst < dev-env > .env
if [[ ! -d migrations ]]; then
    flask db init
    flask db migrate
    flask db upgrade
fi