import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

ENVIRONMENT = os.environ.get("ENVIRONMENT")

class Config(object):
    RECAPTCHA_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "app.db")
    if ENVIRONMENT == "development":
        # THESE KEYS ARE FOR DEVELOPMENT ONLY
        RECAPTCHA_SITE_KEY = "6LcOK5UUAAAAAG23n1PMtQxVGzechf8KVeCQXcqU"
        RECAPTCHA_SECRET_KEY = "6LcOK5UUAAAAAIiBCd3fr3Z4huWTY6oCzKs3ZdSZ"
        SECRET_KEY = "#GuoR^!k*5BEEbLrlP$0nyRekcVY874lyj%AIyViNWM!ZyJ35tmicckEw4EG68dhrEku&MOhfu%3N0&TVI%phW9oTAm7IgE*rGh"
    elif ENVIRONMENT == "production" or ENVIRONMENT == "staging":
        # THESE KEYS ARE FOR STAGING/PRODUCTION ONLY (staging will be moved later)
        RECAPTCHA_SITE_KEY = "6Lf1ZJQUAAAAADfIoSTxiitJ9IEI3hBlnVf5LH1w"
        RECAPTCHA_SECRET_KEY = "6Lf1ZJQUAAAAAIYy8z9z8v30wT_3CxscyyhJE9Lw"
        SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ["paulgwebsite@gmail.com", "paul@paul.systems"]
    REALADMINS = ["paulgwebsite@gmail.com", "paul@paul.systems", "inocencio.adriane@gmail.com"]
    SCHEDULER_API_ENABLED = True
