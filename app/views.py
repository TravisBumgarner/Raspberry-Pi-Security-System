from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm #Imports form from forms.py

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('{} is requesting access to view images for {}...'.format(form.openid.data, form.visit_select.data))
        return redirect('/index')
    return render_template('login.html', form=form)







