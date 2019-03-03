from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, ValidationError

class DBTestForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()])
    submit = SubmitField("Submit")
