
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES, UploadSet, configure_uploads
import os

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

from app import routes