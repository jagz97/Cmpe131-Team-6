from app import db

class Brand (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable=False, unique =True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable=False, unique =True)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String(128), nullable=False)
    address_line_one = db.Column(db.String(256), nullable=False)
    address_line_two = db.Column(db.Integer)
    city = db.Column(db.String(128), nullable=False)
    state_province_region = db.Column(db.String(128), nullable=False)
    zip_postal_code = db.Column(db.String(32), nullable=False)
    country = db.Column(db.String(64), nullable=False)
    user = db.relationship('User', back_populates='Address')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, nullable=False, unique=True)
    email = db.Column(db.String(30), index =True, nullable=False, unique=True)
    password_hash = db.Column(db.String(128)
    shipping_address = db.relationship('Address', back_populates='User', uselist=False)

db.create_all()
