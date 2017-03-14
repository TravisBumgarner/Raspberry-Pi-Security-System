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

@app.route('/')
@app.route('/index')
def index():
    return render_template('index_signedout.html')


@app.route('/web_viewer', methods = ['GET','POST'])
@login_required
def web_viewer():
    gallery = []
    form = ImageFilterForm()
    if form.validate_on_submit():
        # Get the reason for why the current user is visiting by looking at the form data from the last time they logged in.
        current_user_request = User_Request.query.filter_by(user_id=current_user.id).order_by('date desc').limit(1)[0].visit_select
        if current_user.file_access is True and current_user_request != "admin":
            gallery = get_images(form.start_date.data,form.end_date.data, form.sort_order.data) #insert date range into get_images function
        elif(current_user_request == "admin"):
            gallery = []
            flash('Admin access does not permit photo viewing. Please logout and try again.')
        elif(current_user.file_access is False):
            gallery = []
            flash('Account activation is required.')
    return render_template('index_signedin.html',
                           form=form,
                           gallery=gallery)


@app.route('/protected/<path:filename>')
@limiter.exempt
@login_required
def protected(filename):
    path =  os.path.join(os.path.expanduser('~'), 'webapps', 'chs_photo_storage')
    return send_from_directory(path, filename)


@app.route('/register', methods = ['GET','POST'])
@limiter.limit("5 per hour")
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data,
                    email=form.email.data,
                    file_access=False,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        #token = user.generate_confirmation_token()

        flash('You will be notified when your account has been approved.')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods = ['GET','POST'])
@limiter.limit("10 per hour")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() 
        if user is None or user.verify_password(form.password.data) is False:
            flash('Invalid username or password.') 

        elif form.visit_select.data == "admin" and user.admin_access == False:    
            flash('Admin access required for this activity.')

        elif user.file_access is False:
            flash('Account activation is required.')

        elif user is not None and user.verify_password(form.password.data) and user.file_access is True:
            user_request = User_Request(
                date=datetime.datetime.now(),
                visit_select=form.visit_select.data,
                visit_description=form.visit_description.data,
                user_id=user.id
            )
            db.session.add(user_request)
            db.session.commit()
            login_user(user, remember= False)
            return redirect(url_for('web_viewer'))   
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))
