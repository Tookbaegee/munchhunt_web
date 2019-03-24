from flask import Blueprint

bp = Blueprint('adminfiles', __name__)

from app.admin import routes


