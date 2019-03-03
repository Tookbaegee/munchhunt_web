from flask import Blueprint

bp = Blueprint("dbtest", __name__)

from app.dbtest import routes
