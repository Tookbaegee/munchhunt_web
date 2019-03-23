from flask import jsonify, render_template, request, url_for
from app.api import api
from app import db
from app.models import User
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import User

# TODO: change all of the routes to have / at the end for consistency

@api.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

# route for registering a new user
# NOTE: WILL NEED TO ADD SOME KIND OF VERIFICATION FOR THIS!
@api.route("/register", methods=["POST"])
def register_user():
    data = request.get_json() or {}
    if "username" not in data or "email" not in data or "password" not in data:
        return bad_request("Error: username, email, and password requrired.")
    if User.query.filter_by(username=data["username"]).first():
        return bad_request("Error: choose a different username")
    if User.query.filter_by(email=data["email"]).first():
        return bad_request("Error: choose a different email address")
    # verify password
    stuff = validate_password(data["password"])
    if not stuff[0]:
        return bad_request(stuff[1])
    
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers["Location"] = url_for("api.get_user", id=user.id)
    return response

		
def validate_password(password):
    pwd = str(password) 
    if "password" in pwd.lower():
        return False, "Please do not use any form of the password 'password'."
    elif len(pwd) >= 8 and any(ch.isupper() for ch in pwd) and any(ch.islower() for ch in pwd) and any(ch.isdigit() for ch in pwd):
        file = open("app/auth/cracked_passwords.txt", "r")
        for l in file:
            if pwd in l:
                file.close()
                return False, "Your password meets the basic requirements, but was found in a cracked password database. Please use a different one."
        else:
            file.close()
            return True, "Success"
    else:
        return False, "Your password must be at least 8 characters long, have a least one lowercase letter, at least one uppercase letter, and at least one number."
