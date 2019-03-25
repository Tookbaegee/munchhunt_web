from app import app, db
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app.auth.email import send_password_reset_email, send_email_verification_email
import re
import copy

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", "error")
            return redirect(url_for('login'))
        if user.verified:
            login_user(user, remember=form.remember_me.data)
            flash("Login successful for user {}.".format(form.username.data), "success")
            return redirect(url_for("index"))
        else:
            flash("Your email is not verified. Please verify your email.", "error")
            return redirect(url_for('login'))
    return render_template("auth/login.html", title="Sign In", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, admin=False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        send_email_verification_email(user)
        flash('You have successfully registered, but are not verified. Please verify your email by checking your email for a verification email and clicking the link.', "success")
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='Register', form=form)

@app.route("/verify_email/<token>", methods=["GET", "POST"])
def email_verification(token):
    user = User.verify_email_verification_token(token)
    if not user:
        return redirect(url_for("index"))
    user.verified = True
    db.session.commit()
    flash("Your email has been validated!", "success")
    return redirect(url_for("login"))

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
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash("If you have an account, please check your email to reset your password.", "success")
        return redirect(url_for("login"))
    return render_template("auth/reset_password_request.html", title="Reset Password", form=form)

@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for("index"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been successfully reset.", "success")
        return redirect(url_for("login"))
    return render_template("auth/reset_password.html", form=form)
