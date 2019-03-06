from flask import Blueprint

bp = Blueprint("email_list", __name__)

from app.email_list import routes
