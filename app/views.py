from flask import render_template, flash, redirect, url_for, send_from_directory
from flask_login import login_user, logout_user, login_required
from app import app
from .forms import LoginForm, RegistrationForm, ImageFilterForm #Imports form from forms.py
from .functions import get_images
from .models import User, User_Request
from . import db

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
        gallery = get_images(form.start_date.data,form.end_date.data) #insert date range into get_images function
    return render_template('index_signedin.html',
                           form=form,
                           gallery=gallery)

@app.route('/protected/<path:filename>')
@login_required
def protected(filename):
    return send_from_directory('./security_photos', filename)

@app.route('/register', methods = ['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data,
                    email=form.email.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        #token = user.generate_confirmation_token()

        flash('You will be notified when your account has been approved.')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            user_request = User_Request(
                date = datetime.datetime.now(),
                visit_select = form.visit_select.data,
                visit_description = form.visit_description.data,
                user_id = user.id
            )
            db.session.add(user_request)
            db.session.commit()
            login_user(user, remember= False)
            return redirect(url_for('web_viewer'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))






