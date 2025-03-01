from flask import jsonify, g
from app import db
from app.api import api
from app.api.auth import basic_auth

@api.route("/tokens", methods=["POST"])
@basic_auth.login_required
def get_token():
    """
    ..include:: docs/tokens/get_token.md
    """
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({"token" : token})