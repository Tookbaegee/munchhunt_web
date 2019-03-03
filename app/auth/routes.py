from app import app, mongo, argon2, recaptcha
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.auth.user import User
from app.auth.email import send_password_reset_email
from bson import ObjectId
import re
import copy
import jwt

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({"user.username" : form.username.data})
        print(user)
        is_valid = False
        if user:
            userinfo = user["user"]
            _id = user["_id"]
            user_object = User(_id, userinfo)
            pw_hash = user["user"]["password_hash"]
            if pw_hash:
                is_valid = user_object.check_password(form.password.data)
        if user is None or not is_valid:
            flash("Invalid username or password", "error")
            return redirect(url_for('login'))
        login_user(user_object, remember=form.remember_me.data)
        flash("Login successful for user {}.".format(form.username.data), "success")
        return redirect(url_for("index"))
    return render_template("auth/login.html", title="Sign In", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if recaptcha.verify:
        if form.validate_on_submit():
            user_object = User()
            pw_hash = user_object.set_password(form.password_data)
            mongo.db.users.insert_one({"user": {"username" : form.username.data, "email" : form.email.data, "password_hash": pw_hash}})
            flash('You have successfully registered.', "success")
            return redirect(url_for('login'))
    else:
        flash("Please fill out the captcha form.", "error")
    return render_template('auth/register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have successfully logged out.", "success")
    return redirect(url_for('index'))

@app.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({"user.email" : form.email.data})
        if user:
            send_password_reset_email(user)
        flash("If you have an account, please check your email to reset your password.", "success")
        return redirect(url_for("login"))
    return render_template("auth/reset_password_request.html", title="Reset Password", form=form)

@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        print("already logged in!")
        return redirect(url_for("index"))
    user_object = User()
    decoded_id = user_object.verify_reset_password_token(token)
    print(decoded_id)
    user = mongo.db.users.find_one({"_id" : ObjectId(decoded_id)})
    if not user:
        print("user not found")
        return redirect(url_for("index"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        pw_hash = user_object.set_password(form.password.data)
        user["password_hash"] = pw_hash
        mongo.db.users.update_one({"_id" : ObjectId(user["_id"])}, {"$set": {"user.password_hash" : pw_hash}})
        flash("Your password has been successfully reset.", "success")
        return redirect(url_for("login"))
    return render_template("auth/reset_password.html", form=form)
