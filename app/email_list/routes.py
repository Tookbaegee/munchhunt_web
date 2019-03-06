from app import app, db, recaptcha
from flask import request, render_template, flash, redirect, url_for
from app.email_list.forms import EmailForm
from app.models import Business

@app.route("/email_list", methods=["GET", "POST"])
def email_list():
    form = EmailForm()
    if request.method == "POST":
        if recaptcha.verify():
            if form.validate_on_submit():
                if Business.query.filter_by(email=form.email.data).first():
                    flash("You are already signed up for our email list.", "error")
                    return redirect(url_for("index"))
                else: 
                    business_to_add = Business(email=form.email.data)
                    db.session.add(business_to_add)
                    db.session.commit()
                    flash("Thank you for signing up for our email list!", "success")
                    return redirect(url_for("index"))
        else:
            flash("Please fill out the recaptcha form.", "error")
    return render_template("email_list/email_list.html", form=form)

