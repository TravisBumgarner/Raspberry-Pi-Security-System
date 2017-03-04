from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    requests = db.relationship('User_Request', backref= 'user', lazy = 'dynamic')

    def __repr__(self):
        # Tells us out to print objects of this class, used for debugging
        return '<User {}>'.format(self.email)

class User_Request(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime)
    visit_select = db.Column(db.String(50))
    visit_description = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

