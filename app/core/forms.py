from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, ValidationError

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email address", validators=[DataRequired()])
    phone = StringField("Phone", validators=[DataRequired()])
    message = TextAreaField("Message", widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField("Submit")
