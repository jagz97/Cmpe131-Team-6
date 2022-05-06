from sqlalchemy import Column, ForeignKey, false
from app import db
from datetime import datetime
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash, check_password_hash

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
    username = db.Column(db.String(32), nullable=False)


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


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, nullable=False, unique=True)
    email = db.Column(db.String(32), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(300), nullable=False)
    full_name = db.Column(db.String(128))
    address_line_one = db.Column(db.String(256))
    address_line_two = db.Column(db.String(256))
    city = db.Column(db.String(128))
    state_province_region = db.Column(db.String(128))
    zip_postal_code = db.Column(db.String(32))
    country = db.Column(db.String(64))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)


class Review( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, nullable=False)
    rating = db.Column(db.Integer, nullable=false)
    review = db.Column(db.String(8000))
    #product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

class Merchant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(32), nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password =db.Column(db.String(250), nullable=False)

    def __repr__(self):
         return '<Name %r>' % self.name


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

db.create_all()
