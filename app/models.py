
from app import db, app, argon2, login
from flask_login import UserMixin
from datetime import datetime, timedelta
from time import time
import jwt
import base64
import os

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    alias = db.Column(db.String(120), index=True, unique=True)
    latitude = db.Column(db.Float, index=True)
    longitude = db.Column(db.Float, index=True)
    phone = db.Column(db.String(120), index=True)
    price = db.Column(db.String(120), index=True)
    direction = db.Column(db.String(120), index=True)
    time = db.Column(db.Integer)
    hours = db.relationship("Hours", backref=db.backref("restaurant", uselist=False), lazy="dynamic")
    menu = db.relationship("Menu", backref=db.backref("restaurant", uselist=False), lazy="dynamic")

class Hours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # TODO index true for these?? probably, what if need to look up open on mondays?
    sunday = db.Column(db.String(120), index=True)
    monday = db.Column(db.String(120), index=True)
    tuesday = db.Column(db.String(120), index=True)
    wednesday = db.Column(db.String(120), index=True)
    thursday = db.Column(db.String(120), index=True)
    friday = db.Column(db.String(120), index=True)
    saturday = db.Column(db.String(120), index=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"))
    
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menuItems = db.relationship("MenuItem", backref="menu", lazy="dynamic")
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"))

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    description = db.Column(db.String(200), index=True)
    itemType = db.Column(db.String(120), index=True)
    price = db.Column(db.String(120), index=True)
    menu_id = db.Column(db.Integer, db.ForeignKey("menu.id"))

class IngredientInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # should the below be unique?
    name = db.Column(db.String, index=True)
    optional = db.Column(db.Boolean, index=True)
    caution = db.Column(db.Boolean, index=True)

# For email. 
class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, index=True, default=False)
    # for DB authentication
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode("utf-8")
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token
    
    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)
    
    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def set_password(self, password):
        self.password_hash = argon2.generate_password_hash(password)

    def check_password(self, password):
        return argon2.check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in}, 
            app.config["SECRET_KEY"], algorithm="HS256").decode("utf-8")

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])["reset_password"]
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return "<User {}>".format(self.username)