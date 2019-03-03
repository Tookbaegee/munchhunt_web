from app import app, recaptcha, mongo
from flask import request, render_template, flash, redirect, url_for
from app.dbtest.forms import DBTestForm


@app.route("/dbtest", methods=["GET", "POST"])
def db_test():
    form = DBTestForm()
    stuff = mongo.db.stuff.find({})
    if request.method == "POST":
        if recaptcha.verify():
            if form.validate_on_submit():
                name = form.name.data
                content = form.content.data
                mongo.db.stuff.insert({"name" : name, "content" : content })
                flash("Entry added.", "success")
        else:
            flash("Please fill out the recaptcha form.", "error")
    return render_template("dbtest/dbtest.html", form=form, stuff=stuff)

