from app.models import User
from app import login

@login.user_loader
def load_user(user_id):
    print("running" + str(user_id))
    return User.query.filter_by(id=user_id).first()