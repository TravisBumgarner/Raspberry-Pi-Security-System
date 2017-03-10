from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    file_access = db.Column(db.Boolean, default=False, index=True)
    password_hash = db.Column(db.String(128), index=True)
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    requests = db.relationship('User_Request', backref= 'user', lazy = 'dynamic')

    def __repr__(self):
        # Tells us out to print objects of this class, used for debugging
        return '<User {}>'.format(self.name)


class User_Request(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime)
    visit_select = db.Column(db.String(50))
    visit_description = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        # Tells us out to print objects of this class, used for debugging
        return '<User {}>'.format(self.user_id)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))