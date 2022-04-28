from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY = 'you-will-never-know',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

db = SQLAlchemy(app)

from app import routes