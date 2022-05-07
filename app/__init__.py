import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_msearch import Search
from app.helpers import seller_required
from flask_login import LoginManager

"""
Join the directory path
Source:https://python.hotexamples.com/examples/flask/Flask/config%5B%27basedir%27%5D/python-flask-config%5B%27basedir%27%5D-method-examples.html
"""
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='you-will-never-know',
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'test.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

# Flask-Uploads configration provided on Documentation Page
app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(basedir, 'static/img')

# Photo Upload Setup Sourced from FLASK_UPLOADS Documentaion page https://pythonhosted.org/Flask-Uploads/
photos = UploadSet('photos', IMAGES)  # Flask-Uploads Upload Sets
configure_uploads(app, photos)


db = SQLAlchemy(app)


search = Search()
search.init_app(app) # initalize search

"""
login helper that helps manages the curent logged in user
"""
login = LoginManager(app)
login.login_view = 'login'

from app import routes