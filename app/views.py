from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm, RegistrationForm #Imports form from forms.py
from .functions import get_images
from .models import User
from . import db

@app.route('/')
@app.route('/index')
def index():
    logged_in = True
    if logged_in:
        gallery = get_images()
        display_dates = ["2017","2016","2015"]
        return render_template('index_signedin.html',
                               gallery = gallery,
                               logged_in = logged_in,
                               display_dates = display_dates)
    if not logged_in:
        return render_template('index_signedout.html', logged_in = logged_in)


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
        return redirect('/index')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logged_in = False
    return render_template('index_signedout.html', logged_in = logged_in)






