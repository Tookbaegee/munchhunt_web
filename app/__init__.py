from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template
from config import Config
from flask_sitemap import Sitemap
from flask_mail import Mail
from flask_recaptcha import ReCaptcha
from flask_pymongo import PyMongo
from flask_argon2 import Argon2
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app

app = create_app()
app.config.from_object(Config)
ext = Sitemap(app=app)
mail = Mail(app)
recaptcha = ReCaptcha(app=app)
mongo = PyMongo(app)
argon2 = Argon2(app)
login = LoginManager(app)

from app.core import bp as core_bp
app.register_blueprint(core_bp)

from app.dbtest import bp as dbtest_bp
app.register_blueprint(dbtest_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp)
