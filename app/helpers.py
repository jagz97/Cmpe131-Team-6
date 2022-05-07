from flask import redirect, render_template, request, session
from functools import wraps



"""
Decorator to require login for specific routes
https://flask.palletsprojects.com/en/2.1.x/patterns/viewdecorators/
"""
def seller_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

