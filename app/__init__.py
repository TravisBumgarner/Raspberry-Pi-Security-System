from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
login_manager.init_app(app)

from app import views, models