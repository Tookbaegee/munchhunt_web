from app import db
from app.models import User

user = User(username="admin",email="email@example.com", verified=True, admin=True)
user.set_password("password")
db.session.add(user)
db.session.commit()
