from app import app as app
from app import db, photos
from unicodedata import category
from flask import render_template, redirect, url_for, request, flash, session
from app.forms import Products, LoginForm, SignUpForm, ReviewForm, EditUsernameForm, EditPasswordForm, EditEmailForm, AddressForm
from app.models import Brand, Category, AddProduct, User, Review
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import update
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
                             description=description, availablestock=availablestock,
                             image=image, image_1=image_1, image_2=image_2)

        db.session.add(addprod)
        # if form is successfully submitted show success message
        flash(f'Product {form.name.data} has been added')
        db.session.commit()
        return redirect(url_for('addproduct'))

    return render_template('items/product.html', title='title', form=form, brands=brands, categories=categories)


@app.route('/signUp', methods=['GET', 'POST'])
def signup():
    if 'id' not in session or session['id'] == None:
        form = SignUpForm(request.form)
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            password_hash = generate_password_hash(password, method='pbkdf2:sha256')
            full_name = form.full_name.data
            address_line_one = form.address_line_one.data
            address_line_two = form.address_line_two.data
            city = form.city.data
            state_province_region = form.state_province_region.data
            zip_postal_code = form.zip_postal_code.data
            country = form.country.data
            try:
                newuser = User(username=username, email=email, password_hash=password_hash, full_name=full_name,
                               address_line_one=address_line_one, address_line_two=address_line_two,
                               city=city, state_province_region=state_province_region, zip_postal_code=zip_postal_code,
                               country=country)
                db.session.add(newuser)
                session['id'] = User.query.filter(User.username==username).first().id
                session['username'] = username
                session['email'] = email
                db.session.commit()
                flash('Account created for user {}'.format(form.username.data))
            except Exception:
                flash('Username is taken')
                session.pop('id', None)
                session.pop('username', None)
                session.pop('email', None)
                return redirect(url_for('signup'))
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
    return render_template('signUp.html', title='Sign Up', form=form)


@app.route('/product/<product_id>', methods=['GET', 'POST'])
def productpage(product_id):
    product = AddProduct.query.get(product_id)
    if request.form['Rate Product'] == 'Rate Product':
        session['product_id'] = product_id
        if 'username' in session:# if user is logged in, route to review page, otherwise, route to login page
            return redirect(url_for('review'))
        session.pop('product_id', None)
        return redirect(url_for('login'))
    return render_template('items/productDetails.html', title='Product Details', product=product)


@app.route('/product/review', methods=['GET', 'POST'])
def review():
    # if the cancel button is pressed, then route to the product page
    form = ReviewForm(request.form)
    if request.form['Cancel Review'] == 'Cancel Review':
        product_id = db.session['product']
        url = '/product/' + product_id
        session.pop('product_id', None)
        return redirect(url_for(url))
        # if a user is logged in and has selected a product to review, then the review is added
    if request.method == "POST":
        if form.validate_on_submit():
            if 'product_id' in session and 'username' in session:
                product_id = session['product']
                username = session['username']
                reviewExists = False
                # get the old review object if it exists
                product = AddProduct.query.get(product_id)
                #for review in product.reviews:
                #    if review.username == username:
                #            reviewExists == True
                #            review_id = review.id
                rating = form.rating.data
                review = form.review.data
                ## if there is no review, then add a review
                #if not reviewExists:
                newreview = Review(username=username, rating=rating, review=review, product_id=product_id)
                flash(f'Your review has been added')
                #    db.session.add(newreview)
                ## else update the old review
                #else:
                #    oldReview = Review.query.get(review_id)
                #    oldReview.update(dict(rating=rating, review=review))
                url = '/product/' + product_id
                session.pop('product_id', None)
                return redirect(url_for(url))
            else: # the product or the user is not in session, so the page is rerouted to the home page
                return redirect(url_for(''))
    return render_template('items/productReview.html', title='Product Review', form=form)

@app.route('/user/profile/username', methods=['GET', 'POST'])
def editusername():
    if 'id' in session and session['id'] != None:
        user_id = session['id']
        user = User.query.get(user_id)
        form = EditUsernameForm(request.form)
        if form.validate_on_submit():
            new_username = form.username.data
            try:
                user.username = new_username
                db.session.commit()
                session['username'] = new_username
                return redirect(url_for('userprofile'))
            except Exception:
                db.session.rollback()
                flash('The username is taken')
        if 'Cancel' in request.form:
            return redirect(url_for('userprofile'))
    else:
        return redirect(url_for('userprofile'))
    return render_template('editUsername.html', title='Edit Username', form=form, user=user)


@app.route('/user/profile/email', methods=['GET', 'POST'])
def editemail():
    if 'id' in session and session['id'] != None:
        user_id = session['id']
        user = User.query.get(user_id)
        form = EditEmailForm(request.form)
        if form.validate_on_submit():
            new_email = form.email.data
            try:
                user.email = new_email
                db.session.commit()
                session['email'] = new_email
                return redirect(url_for('userprofile'))
            except Exception:
                db.session.rollback()
                flash('Email is already used')
        if 'Cancel' in request.form:
            return redirect(url_for('userprofile'))
    else:
        return redirect(url_for('home'))
    return render_template('editEmail.html', title='Edit Email', form=form, user=user)

@app.route('/user/profile/password', methods=['GET', 'POST'])
def editpassword():
    if 'id' in session and session['id'] != None:
        user_id = session['id']
        user = User.query.get(user_id)
        form = EditPasswordForm(request.form)
        if form.validate_on_submit():
            current_password = form.current_password.data
            confirm_current_password = form.confirm_current_password.data
            new_password = form.new_password.data
            new_password_hash = generate_password_hash(new_password, method='pbkdf2:sha256')
            if current_password == confirm_current_password:
                if check_password_hash(user.password_hash, current_password):
                    user.password_hash = new_password_hash
                    db.session.commit()
                    return redirect(url_for('userprofile'))
                else:
                    flash('The password is incorrect')
            else:
                flash('The two passwords do not match')
        if 'Cancel' in request.form:
            return redirect(url_for('userprofile'))
    else:
        return redirect(url_for('home'))
    return render_template('editPassword.html', title='Edit Password', form=form, user=user)


@app.route('/user/profile/address', methods=['GET', 'POST'])
def editaddress():
    if 'id' in session and session['id'] != None:
        user_id = session['id']
        user = User.query.get(user_id)
        form = AddressForm(request.form)
        if form.validate_on_submit():
            user.full_name = form.full_name.data
            user.address_line_one = form.address_line_one.data
            user.address_line_two = form.address_line_two.data
            user.city = form.city.data
            user.state_province_region = form.state_province_region.data
            user.zip_postal_code = form.zip_postal_code.data
            user.country = form.country.data
            db.session.commit()
            return redirect(url_for('userprofile'))
        if 'Cancel' in request.form:
            return redirect(url_for('userprofile'))
    else:
        return redirect(url_for('home'))
    return render_template('editAddress.html', title='Edit Address', form=form, user=user)

@app.route('/user/profile', methods=['GET', 'POST'])
def userprofile():
    if 'id' in session and session['id'] != None:
        user_id = session['id']
        user = User.query.get(user_id)
        if 'Edit Username' in request.form:
            return redirect(url_for('editusername'))
        if 'Edit Email' in request.form:
            return redirect(url_for('editemail'))
        if 'Edit Password' in request.form:
            return redirect(url_for('editpassword'))
        if 'Edit Address' in request.form:
            return redirect(url_for('editaddress'))
    else:
        return redirect(url_for('home'))
    return render_template('userProfile.html', title='User Profile', user=user)
