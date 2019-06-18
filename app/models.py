
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

sec_keywords = db.Table('sec_keywords',
        db.Column('secondary_keywords_id', db.Integer, db.ForeignKey('secondary_keywords.id'), primary_key=True),
        db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurant.id'), primary_key=True)
        )

ter_keywords = db.Table('ter_keywords',
        db.Column('tertiary_keywords_id', db.Integer, db.ForeignKey('tertiary_keywords.id'), primary_key=True),
        db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurant.id'), primary_key=True)
        )

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
    website = db.Column(db.String(120))
    hours = db.relationship("Hours", backref=db.backref("restaurant", uselist=False), lazy="dynamic")
    menu = db.relationship("Menu", backref=db.backref("restaurant", uselist=False), lazy="dynamic")
    primary_keyword = db.Column(db.String(120), index=True)
    secondary_keywords = db.relationship('SecondaryKeywords', secondary=sec_keywords, lazy='subquery', backref=db.backref('restaurant', lazy=True))
    tertiary_keywords = db.relationship('TertiaryKeywords', secondary=ter_keywords, lazy='subquery', backref=db.backref('restaurant', lazy=True))
    

    def __repr__(self):
        return "<Restaurant: {}>".format(self.name)

class SecondaryKeywords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return "<SecondaryKeywords: {}>".format(self.keyword)

# QUERY: 
# To get secondary keyword based on restaurant:
# SecondaryKeywords.query.filter(SecondaryKeywords.restaurant.any(name="dummy")).first()
# To get restaurant based on keyword: Restaurant.query.filter(Restaurant.secondary_keywords.any(keyword="Wings")).first()
# 

class TertiaryKeywords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return "<TertiaryKeywords: {}>".format(self.keyword)
        

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

    def __repr__(self):
        return "<Hours: {}>".format(self.restaurant.name)
    
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menuItems = db.relationship("MenuItem", backref="menu", lazy="dynamic")
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"))

    def __repr__(self):
        return "<Menu: {}>".format(self.restaurant.name)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    description = db.Column(db.String(200), index=True)
    itemType = db.Column(db.String(120), index=True)
    price = db.Column(db.String(120), index=True)
    menu_id = db.Column(db.Integer, db.ForeignKey("menu.id"))
    pork = db.Column(db.Boolean, index=True)
    white_meat = db.Column(db.Boolean, index=True)
    beef = db.Column(db.Boolean, index=True)
    nuts = db.Column(db.Boolean, index=True)
    crustacean = db.Column(db.Boolean, index=True)
    shellfish = db.Column(db.Boolean, index=True)
    fish = db.Column(db.Boolean, index=True)

    def __repr__(self):
        return "<MenuItem: {}>".format(self.name)

class IngredientInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # should the below be unique?
    name = db.Column(db.String, index=True)
    optional = db.Column(db.Boolean, index=True)
    caution = db.Column(db.Boolean, index=True)

    def __repr__(self):
        return "<IngredientInfo: {}>".format(self.name)

# For email. 
class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return "<Business: {}>".format(self.email)
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, index=True, default=False)
    verified = db.Column(db.Boolean, index=True, default=False)
    register_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # for DB authentication
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    diet = db.relationship("DietPattern", backref=db.backref("user", uselist=False), lazy="dynamic")

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

    def get_email_verification_token(self, expires_in=604800):
        return jwt.encode(
            {"email_verification": self.id, "exp" : time() + expires_in},
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
    
    @staticmethod
    def verify_email_verification_token(token):
        try:
            id = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])["email_verification"]
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return "<User {}>".format(self.username)

class DietPattern(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pork = db.Column(db.Boolean, index=True)
    white_meat = db.Column(db.Boolean, index=True)
    beef = db.Column(db.Boolean, index=True)
    nuts = db.Column(db.Boolean, index=True)
    crustacean = db.Column(db.Boolean, index=True)
    shellfish = db.Column(db.Boolean, index=True)
    fish = db.Column(db.Boolean, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        username = User.query.filter_by(id=self.user_id).first()
        return "<DietPattern: {}\nPork: {}\nWhite Meat: {}\nBeef: {}\nNuts: {}\nCrustacean: {}\nShellfish: {}\nFish: {}>".format(username, self.pork, self.white_meat, self.beef, self.nuts, self.crustacean, self.shellfish, self.fish)
    