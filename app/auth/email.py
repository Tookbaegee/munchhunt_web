from app import app
from flask import render_template, current_app
from app.email import send_email
from app.auth.user import User
from time import time
import jwt

def send_password_reset_email(user):
    # token = user.get_reset_password_token()
    # create password token with ID of user
    # get email of user

    user_object = User(user["_id"], user["user"])
    token = user_object.get_reset_password_token()
    #token = jwt.encode({"reset_password": str(user["_id"]), "exp": time() + 600}, app.config["SECRET_KEY"], algorithm="HS256").decode("utf-8")
    send_email("[Paul's Flask Site] Reset Your Password",
                sender=current_app.config["ADMINS"][0],
                recipients=[user["user"]["email"]],
                text_body=render_template("email/reset_password.txt", user=user, token=token),
                html_body=render_template("email/reset_password.html", user=user , token=token)
    )
