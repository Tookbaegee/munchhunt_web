from app import db, scheduler
from app.models import User
from time import time

@scheduler.task("cron", id="delete_unverified", minute=1)
def delete_unverified():
    users = User.query.filter_by(verified=False)
    for u in users:
        if u.register_time.timestamp() + 604800 < time():  
            db.session.delete(u)
    db.session.commit()