from flask import render_template, flash, redirect, url_for, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from app import app
from .forms import LoginForm, RegistrationForm, ImageFilterForm #Imports form from forms.py
from .functions import get_images
from .models import User, User_Request
from . import db
from app import limiter

import datetime
import os


@app.route('/', methods = ['GET','POST'])
@limiter.limit("10 per hour")
def index():
    login_form = LoginForm()
    registration_form = RegistrationForm()

    if login_form.login.data and login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is None or user.verify_password(login_form.password.data) is False:
            flash('Invalid username or password.')

        elif login_form.visit_select.data == "admin" and user.admin_access == False:
            flash('Admin access required for this activity.')

        elif user.file_access is False:
            flash('Account activation is required.')

        if user is not None and user.verify_password(login_form.password.data) and user.file_access is True:
            user_request = User_Request(
                date=datetime.datetime.now(),
                visit_select=login_form.visit_select.data,
                visit_description=login_form.visit_description.data,
                user_id=user.id
            )
            db.session.add(user_request)
            db.session.commit()
            login_user(user, remember= False)
            return redirect(url_for('web_viewer'))

    if registration_form.register.data and registration_form.validate_on_submit():
        user = User(name=registration_form.name.data,
                    email=registration_form.email.data,
                    file_access=False,
                    password = registration_form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('You will be notified when your account has been approved.')
        return redirect(url_for('index'))

    return render_template('index.html', login_form=login_form, registration_form=registration_form)


@limiter.limit("100 per hour")
@app.route('/web_viewer', methods = ['GET','POST'])
@login_required
def web_viewer():
    gallery = []
    form = ImageFilterForm()
    if form.validate_on_submit():
        # Get the reason for why the current user is visiting by looking at the form data from the last time they logged in.
        current_user_request = User_Request.query.filter_by(user_id=current_user.id).order_by('date desc').limit(1)[0].visit_select
        if current_user.file_access is True and current_user_request != "admin":
            gallery = get_images(form.start_date.data,form.end_date.data) #insert date range into get_images function
        elif(current_user_request == "admin"):
            gallery = []
            flash('Admin access does not permit photo viewing. Please logout and try again.')
        elif(current_user.file_access is False):
            gallery = []
            flash('Account activation is required.')
    return render_template('web_viewer.html',
                           form=form,
                           gallery=gallery)


@app.route('/protected/<image_date>/<image_hour>/<file_name>')
@limiter.exempt
@login_required
def protected(image_date, image_hour, file_name):
    path = os.path.join(os.path.expanduser('~'),'webapps','chs_photo_storage', image_date, image_hour)
    return send_from_directory(path, file_name)


@app.route('/protected/thumbs/<image_date>/<image_hour>/<file_name>')
@limiter.exempt
@login_required
def protected_thumbs(image_date, image_hour, file_name):
    path = os.path.join(os.path.expanduser('~'),'webapps','chs_photo_storage', 'thumbs', image_date, image_hour)
    return send_from_directory(path, file_name)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))
