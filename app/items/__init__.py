from app import db

class Brand(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    