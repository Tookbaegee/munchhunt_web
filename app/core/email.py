from flask import render_template, current_app
from app.email import send_email

def send_form_email(name, email, phone, message):
    send_email("[Munch Hunt Website] New Form Notification",
                sender=current_app.config["ADMINS"][0],
                recipients=current_app.config["ADMINS"],
                text_body=render_template("email/form_message.txt",name=name, email=email, phone=phone, message=message),
                html_body=render_template("email/form_message.html", name=name, email=email, phone=phone, message=message)
)
