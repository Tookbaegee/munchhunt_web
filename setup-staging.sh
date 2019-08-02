echo "Please install packages manually for staging/prod."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
envsubst < staging-env > .env
if [[ ! -d migrations ]]; then
    flask db init
    flask db migrate
    flask db upgrade
fi