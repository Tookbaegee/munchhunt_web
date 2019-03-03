from app import app, argon2, login, mongo
from flask_login import UserMixin
from datetime import datetime
from time import time
import jwt
from bson import ObjectId

@login.user_loader
def load_user(id):
    return User(id, mongo.db.users.find_one({"_id" : ObjectId(id)})["user"])

class User(UserMixin):
    def __init__(self, id=None, userinfo=None):
        if userinfo:
            self.id = str(id)
            self.username = userinfo["username"]
            self.email = userinfo["email"]
            self.password_hash = userinfo["password_hash"]
        else:
            self.password_hash = None
    
    def set_password(self, password):
        self.password_hash = argon2.generate_password_hash(password)
        return self.password_hash

    def check_password(self, password):
        return a    print(str(user_object.id))gon2.check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        print("using ID: " + self.id)
        return jwt.encode(
            {"reset_password": str(self.id), "exp": time() + expires_in}, 
            app.config["SECRET_KEY"], algorithm="HS256").decode("utf-8")
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            _id = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])["reset_password"]
        except:
            return
        return _id

    def __repr__(self):
        return "<User {}>".format(self.username)