from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
import re

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        # elif len(email.data) > 7:
        #     if re.match(r"^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email) == None:
        #         raise ValidationError("Email address is invalid.")
    
    def validate_password(self, password):
        pwd = str(password.data) 
        if "password" in pwd.lower():
            raise ValidationError("Please do not use any form of the password 'password'.")
        elif len(pwd) >= 8 and any(ch.isupper() for ch in pwd) and any(ch.islower() for ch in pwd) and any(ch.isdigit() for ch in pwd):
            file = open("app/auth/cracked_passwords.txt", "r")
            for l in file:
                if pwd in l:
                    file.close()
                    raise ValidationError("Your password meets the basic requirements, but was found in a cracked password database. Please use a different one.")
            else:
                file.close()
                return
        else:
            raise ValidationError("Your password must be at least 8 characters long, have a least one lowercase letter, at least one uppercase letter, and at least one number.")

class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")
