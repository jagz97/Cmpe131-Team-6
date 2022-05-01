from app import app as app
from app import db, photos
from unicodedata import category
from flask import render_template, redirect, url_for, request, flash
from app.forms import Products
from app.models import Brand, Category, AddProduct
from flask_wtf import FlaskForm
from wtforms import StringField


@app.route('/')
def home():
    products = AddProduct.query.filter(AddProduct.availablestock > 0)

    return render_template('home.html', products=products)


@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The brand {getbrand} has been added', 'success')
        db.session.commit()
        return redirect(url_for('addproduct'))

    return render_template('items/brand.html', brand='brand')


@app.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    if request.method == "POST":
        getcat = request.form.get('category')
        category = Category(name=getcat)
        db.session.add(category)
        flash(f'The category {getcat} has been added', 'success')
        db.session.commit()
        return redirect(url_for('addproduct'))

    return render_template('items/brand.html')


@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Products(request.form)
    if request.method == 'POST':
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        description = form.description.data
        availablestock = form.availableStock.data
        brand = request.form.get('brand')
        category = request.form.get('category')

        # receiving photo from form
        image = photos.save(request.files['photo'])
        # receiving photo1 from form
        image_1 = photos.save(request.files['photo1'])
        # receiving photo2 from form
        image_2 = photos.save(request.files['photo2'])

        addprod = AddProduct(name=name, price=price, category_id=category, brand_id=brand, discount=discount,
                             description=description, availablestock=availablestock, image=image, image_1=image_1, image_2=image_2)

        db.session.add(addprod)
        # if form is successfully submitted show success message
        flash(f'Product {form.name.data} has been added')
        db.session.commit()
        return redirect(url_for('addproduct'))

    return render_template('items/product.html', title='title', form=form, brands=brands, categories=categories)
