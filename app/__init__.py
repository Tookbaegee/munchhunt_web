import psutil
from flask import Flask, abort
from flask_bootstrap import Bootstrap
from flask import render_template
from config import Config
from flask_sitemap import Sitemap
from flask_mail import Mail
from flask_recaptcha import ReCaptcha
from flask_argon2 import Argon2
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_apscheduler import APScheduler

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
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
@app.before_first_request
def load_tasks():
    from app.tasks import delete_unverified

from app.core import bp as core_bp
app.register_blueprint(core_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp)

from app.email_list import bp as email_list_bp
app.register_blueprint(email_list_bp)

# there may be multiple APIs in the future but this is good for now
from app.api import api
app.register_blueprint(api, url_prefix="/api")

class AdminView(AdminIndexView):
    @expose("/")
    def adminindex(self):
        if not current_user.is_authenticated:
            abort(404)
        else:
            if current_user.admin:
                sysinfo = []
                raminfo = psutil.virtual_memory()
                diskinfo = psutil.disk_usage("/")
                sysinfo.extend((
                    {"cpu": psutil.cpu_percent()},
                    {"cpu_cores" : psutil.cpu_count(logical=False)},
                    {"cpu_threads":psutil.cpu_count(logical=True)},
                    {"cpu_freq":round(psutil.cpu_freq().current / 10 ** 3, 2)} if psutil.cpu_freq() else None,
                    {"ram_percent":raminfo.percent},
                    {"ram_used":round(raminfo.used / 10 ** 9, 4,)},
                    {"ram_free": round(raminfo.free / 10 ** 9, 4)},
                    {"ram_total":round(raminfo.total / 10 ** 9, 4)},
                    {"disk_percent":diskinfo.percent},
                    {"disk_used":round(diskinfo.used / 10 ** 9, 4)},
                    {"disk_total":round(diskinfo.total / 10 ** 9, 4)},
                    {"disk_free":round(diskinfo.free / 10 ** 9, 4)}
                ))
                for item in sysinfo:
                    if item:
                        itemname = list(item.keys())[0]
                        self._template_args[itemname] = item[itemname]

                return super(AdminView, self).index()
            else:
                abort(404) 

class MyModelView(ModelView):
    can_delete = True
    page_size = 50

from app.models import Restaurant, Menu, MenuItem, Hours, IngredientInfo, Business, User, SecondaryKeywords, TertiaryKeywords, DietPattern

admin = Admin(app, name="Munch Hunt Administration", index_view=AdminView(), template_mode="bootstrap3")

models = [Restaurant, Menu, MenuItem, Hours, IngredientInfo, Business, User, SecondaryKeywords, TertiaryKeywords, DietPattern]
for model in models:
    admin.add_view(MyModelView(model, db.session))

from app.admin import bp as admin_bp
app.register_blueprint(admin_bp)

from app.admin import routes