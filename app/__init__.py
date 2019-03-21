from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template
from config import Config
from flask_sitemap import Sitemap
from flask_mail import Mail
from flask_recaptcha import ReCaptcha
from flask_argon2 import Argon2
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app

app = create_app()
app.config.from_object(Config)
ext = Sitemap(app=app)
mail = Mail(app)
recaptcha = ReCaptcha(app=app)
argon2 = Argon2(app)
login = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.core import bp as core_bp
app.register_blueprint(core_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp)

from app.email_list import bp as email_list_bp
app.register_blueprint(email_list_bp)

# there may be multiple APIs in the future but this is good for now
from app.api import api
app.register_blueprint(api, url_prefix="/api")