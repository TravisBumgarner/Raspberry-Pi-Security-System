from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from threading import Thread
from .functions import generate_thumbnails

app = Flask(__name__)
app.config.from_object('config')

# Flask_sqlalchemy
db = SQLAlchemy(app)

# Flask_Login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

# Flask_Admin
admin = Admin(app)

# Flask Limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    global_limits=["200 per day", "50 per hour"]
)

# Thumbnails
Thread(target = generate_thumbnails).start()

from app import views, models, admin_panel

if __name__ == '__main__':
    app.run(debug=False)
