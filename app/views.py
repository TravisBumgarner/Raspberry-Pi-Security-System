from flask import render_template, flash, redirect
from flask_login import login_user, logout_user, login_required
from app import app
from .forms import LoginForm, RegistrationForm, ImageFilterForm #Imports form from forms.py
from .functions import get_images
from .models import User
from . import db

@app.route('/')
@app.route('/index')
def index():
    return render_template('index_signedout.html')

@app.route('/web_viewer', methods = ['GET','POST'])
def web_viewer():
    gallery = []
    form = ImageFilterForm()
    test_string = 'Before Post'
    if form.validate_on_submit():
        gallery = get_images(form.start_date.data,form.end_date.data) #insert date range into get_images function
        test_string = 'Getting photos for dates between {} and {}'.format(form.start_date.data, form.end_date.data)
    return render_template('index_signedin.html',
                           form=form,
                           test_string = test_string,
                           gallery=gallery)

@app.route('/register', methods = ['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data,
                    email=form.email.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You will be notified when your account has been approved.')
        return redirect('/index')
    return render_template('register.html', form=form)


@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember= False)
            return redirect('/web_viewer')
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect('/index')






