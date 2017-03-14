# Imports
import os

# SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# WTForms
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# Flask Thumbnails
MEDIA_FOLDER = "./app/security_photos"
MEDIA_URL = "/static/"



