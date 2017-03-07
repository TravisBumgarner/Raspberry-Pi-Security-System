from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm #Imports form from forms.py
from .functions import get_images


@app.route('/')
@app.route('/index')
def index():
    logged_in = True
    if logged_in:
        gallery = get_images()
        return render_template('index_signedin.html',gallery = gallery, logged_in = logged_in)
    if not logged_in:
        return render_template('index_signedout.html', logged_in = logged_in)

@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('{} is requesting access to view images for {}...'.format(form.openid.data, form.visit_select.data))
        return redirect('/index')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logged_in = False
    return render_template('index_signedout.html', logged_in = logged_in)






