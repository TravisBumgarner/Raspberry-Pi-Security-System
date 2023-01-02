from app import db
from flask_admin.contrib import sqla
from flask import redirect, url_for, flash
import flask_login
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView, expose
from app import app
from .models import User, User_Request

class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        last_request = User_Request.query.order_by(User_Request.date.desc()).limit(1).all()[0]
        total_issues = len(User_Request.query.all())
        last_login_user = User.query.filter_by(id = last_request.user_id).limit(1).all()[0].name
        last_login_date = last_request.date
        last_login_reason = last_request.visit_description

        return self.render('admin/index.html',
                           total_issues = len(User_Request.query.all()),
                           last_login_user = last_login_user,
                           last_login_date = last_login_date,
                           last_login_reason = last_login_reason)

admin = Admin(app, index_view=MyHomeView())


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
        return redirect(url_for('index'))



admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(User_Request, db.session))

