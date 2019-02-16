from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template
from config import Config
from flask_sitemap import Sitemap
from flask_mail import Mail

def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app

app = create_app()
app.config.from_object(Config)
ext = Sitemap(app=app)
mail = Mail(app)

from app.core import bp as core_bp
app.register_blueprint(core_bp)
