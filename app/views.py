from flask import render_template, flash, redirect
from flask_login import login_user, logout_user, login_required
from app import app
from .forms import LoginForm, RegistrationForm #Imports form from forms.py
from .functions import get_images
from .models import User
from . import db

@app.route('/')
@app.route('/index')
def index():
    gallery = get_images()
    display_dates = ["2017","2016","2015"]
    return render_template('index_signedin.html',
                           gallery = gallery,
                           display_dates = display_dates)


@app.route('/register', methods = ['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data,
                    email=form.email.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect('/index')
    return render_template('register.html', form=form)


@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('{} is requesting access to view images for {}...'.format(form.email.data, form.visit_select.data))
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember= False)
            return redirect('/index')
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect('/index')






