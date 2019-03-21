sudo ./addpostgresql.sh
sudo apt install python3
sudo apt install python3-venv
sudo apt install python3-pip
sudo apt install postgresql-11
sudo -su postgresql
echo "PLEASE ENTER A PASSWORD!"
# if there is a way to avoid using md5 that would be epic
createuser -S -D -R -e -P munchhunt
# is this needed?
createdb munchhunt
exit
python3 -m venv venv
source venv/bin/activate
pip install wheel flask flask-wtf python-dotenv flask-bootstrap4 flask-mail flask-sitemap flask-recaptcha flask-sqlalchemy flask-migrate flask-login flask-argon2 pyjwt autoenv psycopg2-binary flask-restful flask-httpauth
if [[ ! -d migrations ]]; then
    flask db init
    flask db migrate
    flask db upgrade
fi