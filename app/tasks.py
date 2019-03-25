from app import db, scheduler
from app.models import User
from time import time

@scheduler.task("cron", id="delete_unverified", hour=1)
def delete_unverified():
    print("deleting unverified users")
    users = User.query.filter_by(verified=False)
    for u in users:
        if u.register_time + 604800 < time():  
            print(u.username + " deleted.")
            db.session.delete(u)
        else:
            print(u.username + " is unverified but still has time left to verify.")
    db.session.commit()