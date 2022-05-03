from app import app as app
from app import db, photos
from unicodedata import category
from flask import render_template, redirect, url_for, request, flash
from app.forms import Products, LoginForm, SignUpForm, ReviewForm
from app.models import Brand, Category, AddProduct, User, Review
from flask_wtf import FlaskForm
from wtforms import StringField
from hashlib import md5
from sqlalchemy import exc

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


@app.route('/signUp', methods=['GET', 'POST'])
def signup():
    db.session['id'] = None
    db.session['username'] = None
    db.session['email'] = None
    form = SignUpForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            password_hash = md5(password.encode())
            is_merchant = form.isMerchant.data
            newuser = User(username=username, email=email, password_hash=password_hash, is_merchant=is_merchant)
            try:
                db.session.add(newuser)
                user = User.query.filter_by(username=username).first()
                db.session['id'] = user.id
                db.session['username'] = username
                db.session['email'] = email
                flash('Account created for user {}'.format(form.username.data))
                return redirect(url_for('/'))
            except exc.SQLAlchemyError as e:
                db.session.rollback()
                print(type(e))
    return render_template('signUp.html', title='Sign Up', form=form)


@app.route('/product/<product_id>', methods=['GET', 'POST'])
def productpage(product_id):
    product = AddProduct.query.get(product_id)
    if request.form['rate_button'] == 'Rate Product':
        db.session['product_id'] = product_id
        if 'username' in db.session:# if user is logged in, route to review page, otherwise, route to login page
            return redirect(url_for('/product/review'))
        db.session['product_id'] = None
        return redirect(url_for('/login'))
    return render_template('productDetails.html', title='Product Details', product=product)


@app.route('/product/review', methods=['GET', 'POST'])
def review():
    # if the cancel button is pressed, then route to the product page
    form = ReviewForm(request.form)
    if request.form['cancel_button'] == 'Cancel review':
        product_id = db.session['product']
        url = '/product/' + product_id
        db.session['product_id'] = None
        return redirect(url_for(url))
        # if a user is logged in and has selected a product to review, then the review is added
    if request.method == "POST":
        if form.validate_on_submit():
            if 'product_id' in db.session and 'username' in db.session:
                product_id = db.session['product']
                username = db.session['username']
                reviewExists = False
                # get the old review object if it exists
                product = AddProduct.query.get(product_id)
                for review in product.reviews:
                    if review.username == username:
                            reviewExists == True
                            review_id = review.id
                rating = form.rating.data
                review = form.review.data
                # if there is no review, then add a review
                if not reviewExists:
                    newreview = Review(username=username, rating=rating, review=review, product_id=product_id)
                    flash(f'Your review has been added')
                    db.session.add(newreview)
                # else update the old review
                else:
                    oldReview = Review.query.get(review_id)
                    oldReview.update(dict(rating=rating, review=review))
                url = '/product/' + product_id
                db.session['product_id'] = None
                return redirect(url_for(url))
            else: # the product or the user is not in session, so the page is rerouted to the home page
                return redirect(url_for(''))
    return render_template('productDetails.html', title='Product Review')



