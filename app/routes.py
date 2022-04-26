from flask import render_template

from app import app,db

@app.route('/')
def method_name():
    return "Home Page of Amazin"