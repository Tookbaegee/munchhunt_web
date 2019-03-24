from flask import url_for, redirect, abort
from app.models import User
from flask_admin import AdminIndexView, helpers, expose
from flask_login import current_user

class AdminView(AdminIndexView):
    @expose("/")
    def adminindex(self):
        if not current_user.is_authenticated:
            abort(404)
        else:
            if current_user.admin:
                return super(AdminView, self).index()
            else:
                abort(404) 
