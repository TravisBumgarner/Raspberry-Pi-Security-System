from app import db, admin
from flask_admin.contrib import sqla
from flask import redirect, url_for, flash
import flask_login
from app.models import User, User_Request
from flask_admin.contrib.sqla import ModelView



class AdminModelView(sqla.ModelView):
    def is_accessible(self):
        try:
            admin_access = flask_login.current_user.admin_access
            logged_in = flask_login.current_user.is_authenticated
            return admin_access and logged_in
        except:
            return False


    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))


admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(User_Request, db.session))