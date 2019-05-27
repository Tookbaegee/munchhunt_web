from app import app, recaptcha
from app.models import User
from flask import request, render_template, flash, redirect, url_for, abort, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from app.core.forms import ContactForm
from app.core.email import send_form_email
import sys

@app.route("/", methods=["GET", "POST"])
def index():
    form = ContactForm()
    if request.method == "POST":
        if recaptcha.verify():
            if form.validate_on_submit():
                try:
                    send_form_email(name=form.name.data, email=form.email.data, phone=form.phone.data, message=form.message.data)
                    flash("Email sent.", "success")
                except:
                    e = sys.exc_info()[0]
                    print("Error: %s" % e)
                    flash("Email failed to send due to an internal server error. We will resolve this ASAP!", "error")
                    
        else:
            flash("Please fill out the recaptcha form.", "error")
    return render_template("core/index.html", form=form)

@app.route("/restaurants")
def restaurants():
    return render_template("core/restaurants.html")

@app.route("/team")
def team():
    return render_template("core/team.html")

@login_required
@app.route("/docs/")
def docs():
    if current_user.admin:
        return send_from_directory('static/docs/', "index.html", as_attachment=False)
    else:
        abort(404)

@login_required
@app.route("/docs/<path:path>")
def docs_path(path):
    if current_user.admin:
        return send_from_directory('static/docs/', path, as_attachment=False)
    else:
        abort(404)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if request.method == "POST":
        if recaptcha.verify():
            if form.validate_on_submit():
                try:
                    send_form_email(name=form.name.data, email=form.email.data, phone=form.phone.data, message=form.message.data)
                    flash("Email sent.", "success")
                except:
                    e = sys.exc_info()[0]
                    print("Error: %s" % e)
                    flash("Email failed to send due to an internal server error. We will resolve this ASAP!", "error")
        else:
            flash("Please fill out the recaptcha form.", "error")
    return render_template("core/contact.html", form=form)
