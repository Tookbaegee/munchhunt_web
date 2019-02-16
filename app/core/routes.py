from app import app
from flask import render_template, flash, redirect, url_for
from app.core.forms import ContactForm
from app.core.email import send_form_email

@app.route("/", methods=["GET", "POST"])
def index():
    form = ContactForm()
    if form.validate_on_submit():
        send_form_email(name=form.name.data, email=form.email.data, phone=form.phone.data, message=form.message.data)
        flash("Email sent.", "success")
    return render_template("core/index.html", form=form)

@app.route("/restaurants")
def restaurants():
    return render_template("core/restaurants.html")

@app.route("/team")
def team():
    return render_template("core/team.html")

@app.route("/contact")
def contact():
    return render_template("core/contact.html")
