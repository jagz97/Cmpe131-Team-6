from sqlalchemy import Column, ForeignKey, false
from app import db
from datetime import datetime

# Source Code: Simple Relations https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/


class AddProduct(db.Model):
    __searchable__= ['name','description']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    discount = db.Column(db.Integer, default=0)
    # Integer with 2 decimal places
    price = db.Column(db.Numeric(10, 2), nullable=False)
    availablestock = db.Column(db.Integer, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)
    category = db.relationship(
        'Category', backref=db.backref('categories', lazy=True))

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    brand = db.relationship('Brand', backref=db.backref('brands', lazy=True))

    image = db.Column(db.String(150), nullable=False)
    image_1 = db.Column(db.String(150), nullable=False)
    image_2 = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return '<AddProduct %r>' % self.name


class Brand (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String(128), nullable=False)
    address_line_one = db.Column(db.String(256), nullable=False)
    address_line_two = db.Column(db.Integer)
    city = db.Column(db.String(128), nullable=False)
    state_province_region = db.Column(db.String(128), nullable=False)
    zip_postal_code = db.Column(db.String(32), nullable=False)
    country = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, nullable=False, unique=True)
    email = db.Column(db.String(30), index =True, nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    shipping_addresses = db.relationship('Address', backref="user", lazy='dynamic')

db.create_all()

