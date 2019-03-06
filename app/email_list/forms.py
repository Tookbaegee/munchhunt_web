from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, ValidationError

class EmailForm(FlaskForm):
    email = StringField("Email address", validators=[DataRequired()])
    submit = SubmitField("Submit")
