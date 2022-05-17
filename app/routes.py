import secrets

from flask import render_template, redirect, url_for, request, flash, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from app import app as app
from app import db, photos
from app.forms import Products, LoginForm, SignUpForm, ReviewForm, EditUsernameForm, EditPasswordForm, EditEmailForm, \
    AddressForm, MerchantSignup, MerchantLogin
from app.helpers import seller_required
from app.models import Brand, Category, AddProduct, User, Review, Merchant, CustomerOrder
import stripe
import requests

publishable_key = 'pk_test_51KxjFzLGavGifIHgE46wfoXUQnSmanRC0rX6KRsL6iH0gII3LZ1INayMe0nH51wIJdakCyEwhEoux6tjphnPIbnm00gWEU1Qcx'

stripe.api_key = 'sk_test_51KxjFzLGavGifIHgiMdIOOdRlyHLKg0elxsL5iStElwzlbGrboQmH7RHtS1CJ8VxmZ2IrefIiCjPjZpNqNwG1Aep00kaUCU9cP'


def subscribe_user(email, user_group_email, api_key):
    """
    Function that lets users to sign up to receive newsletter
    """
    resp = requests.post(f"https://api.mailgun.net/v3/lists/{user_group_email}/members",
                         auth=("api", api_key),
                         data={"subscribed": True,
                               "address": email}
                         )

    print(resp.status_code)

    return resp


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Splash Page connected to API that lets users signup for newsletter
    """
    if request.method == "POST":
        email = request.form.get('email')

        subscribe_user(email=email,
                       user_group_email="newsletter_products@sandbox7e131a1ce3fb434b96be63819cbf91d7.mailgun.org",
                       api_key="6a30bb50eb9c8816d250c1ecf7b87302-5e7fba0f-3eccfe0c")
        requests.post(
            "https://api.mailgun.net/v3/sandbox7e131a1ce3fb434b96be63819cbf91d7.mailgun.org/messages",
            auth=("api", "6a30bb50eb9c8816d250c1ecf7b87302-5e7fba0f-3eccfe0c"),
            data={"from": "Excited User <mailgun@sandbox7e131a1ce3fb434b96be63819cbf91d7.mailgun.org>",
                  "to": ["newsletter_products@sandbox7e131a1ce3fb434b96be63819cbf91d7.mailgun.org", "mailgun@sandbox7e131a1ce3fb434b96be63819cbf91d7.mailgun.org"],
                  "subject": "Hello",
                  "text": "You've been subscribed!"})
        return redirect(url_for('home'))

    return render_template('index.html')


@app.route('/payments', methods=['GET', 'POST'])
def payment():
    """
    Stripe payment setup for secure checkout
    Source: https://stripe.com/docs/payments/checkout/migration
    """
    amount = request.form.get('amount')
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        description='Shop Orders',
        amount=amount,
        currency='usd',
    )
    return redirect(url_for('success'))


@app.route('/success')
def success():
    """
    Success message display upon successful payment
    """
    return render_template('success.html')


@app.route('/home')
def home():
    """
    Route to the home page of the application
    """
    products = AddProduct.query.filter(AddProduct.availablestock > 0)

    return render_template('home.html', products=products)


@app.route('/result')
def result():
    """
    Returns the items searched from added products
    Created search functionality using m-search
    Source: https://github.com/honmaple/flask-msearch
    """
    searchword = request.args.get('q')
    products = AddProduct.query.msearch(searchword, fields=['name', 'description'], limit=3)

    return render_template('search.html', products=products)


@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    """
    Retrieves the information from add brand form and adds it to the database
    """
    if request.method == "POST":
        try:
            getbrand = request.form.get('brand')
            brand = Brand(name=getbrand)
            db.session.add(brand)
            db.session.commit()
            flash(f'The brand {getbrand} has been added', 'success')
            return redirect(url_for('addproduct'))
        except Exception:
            flash(f'The brand {getbrand} already exists')
            return redirect(url_for('addproduct'))
    return render_template('items/brand.html', brand='brand')


@app.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    """
    Retrieves the information from add product form and adds it to the database
    """
    if request.method == "POST":
        try:
            getcat = request.form.get('category')
            category = Category(name=getcat)
            db.session.add(category)
            db.session.commit()
            flash(f'The category {getcat} has been added', 'success')
            return redirect(url_for('addproduct'))
        except Exception:
            flash(f'The category {getcat} already exist')
            return redirect(url_for('addproduct'))

    return render_template('items/brand.html')


@app.route('/addproduct', methods=['GET', 'POST'])
@seller_required
def addproduct():
    """
    Retrieves the information from add product form and adds it to the database
    """
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

        try:
            # receiving photo from form
            image = photos.save(request.files.get('image'))
            # receiving photo1 from form
            image_1 = photos.save(request.files.get('image_1'))
            # receiving photo2 from form
            image_2 = photos.save(request.files.get('image_2'))
        except Exception:
            flash(f'Files need to be photos only. Supported type: jpg, jpeg, png, gif')
            return redirect(url_for('addproduct'))

        addprod = AddProduct(name=name, price=price, category_id=category, brand_id=brand, discount=discount,
                             description=description, availablestock=availablestock, image=image, image_1=image_1,
                             image_2=image_2, username=session['username'])

        db.session.add(addprod)
        # if form is successfully submitted show success message
        flash(f'Product {form.name.data} has been added')
        db.session.commit()
        rows = AddProduct.query.filter_by(username=session['username'])
        return render_template('items/product.html', title='title', form=form, brands=brands, categories=categories,
                               rows=rows)
    rows = AddProduct.query.filter_by(username=session['username'])
    return render_template('items/product.html', title='title', form=form, brands=brands, categories=categories,
                           rows=rows)


@app.route('/signupmerchant', methods=['GET', 'POST'])
def signup_merchant():
    """
    Creates the route for merchant signup form and retrievs the data, add it to the database
    """
    form = MerchantSignup(request.form)
    if request.method == "POST":
        session.clear()
        password = form.password.data
        reenter = form.reenter.data
        if (password != reenter):
            flash('Passwords do not match')
            return redirect(url_for('signup_merchant'))

        # passwordHash
        pass_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        fullname = form.fullname.data
        username = form.username.data

        # db store
        new_usr = Merchant(fullname=fullname, username=username, password=pass_hash)
        try:
            db.session.add(new_usr)
            db.session.commit()
        except:
            flash('User Name already taken')
            return redirect(url_for('signup_merchant'))
        return redirect(url_for('login_merchant'))

    return render_template("merchantsignup.html", form=form)


@app.route('/merchantlogin', methods=['GET', 'POST'])
def login_merchant():
    """
    Login Page for merchant
    """
    form = MerchantLogin(request.form)
    if request.method == 'POST':
        session.clear()
        username = form.fullname.data
        password = form.password.data
        result = Merchant.query.filter_by(username=username).first()
        # checking if username exist and password entered it correct
        if result == None or not check_password_hash(result.password, password):
            flash('Username or Password Incorrect. Please try again')
            return redirect(url_for('login_merchant'))

        # remember the logged in user
        session["username"] = result.username
        return redirect(url_for('addproduct'))
    return render_template('merchantlogin.html', form=form)


@app.route('/merchantlogout')
def logut_merchant():
    """
    Logs out the signed in merchant and redirects to login page
    """
    session.clear()
    flash('You have been logged out.Login again?')
    return redirect(url_for('login_merchant'))


@app.route('/addcart', methods=['POST', 'GET'])
def AddCart():
    """
    Add items to cart
    Lets user add item to cart and keep tracks of it while the user is in session
    """
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        product = AddProduct.query.filter_by(id=product_id).first()
        if product_id and quantity and request.method == "POST":
            ditems = {product_id: {'name': product.name, 'price': product.price, 'discount': product.discount,
                                   'quantity': quantity, 'image': product.image}}
        if 'Cart' in session:
            print(session['Cart'])
            if product_id in session['Cart']:
                flash("Item already in cart")
            else:
                session['Cart'] = Merge(session['Cart'], ditems)
                return redirect(request.referrer)
        else:
            session['Cart'] = ditems
            return redirect(request.referrer)
    except Exception as e:
        flash("Failed, Please try again")
    finally:
        return redirect(request.referrer)


def Merge(dict1, dict2):
    """
    This function takes two dict and merges them to create one single dict
    Manages the items being added to cart
    """
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


@app.route('/cart')
def getCart():
    """
    Retrieves items from cart
    """
    if 'Cart' not in session or len(session['Cart']) <= 0:  # check if cart has items
        return redirect(url_for('home'))
    subtotal = 0
    g_total = 0
    for key, product in session['Cart'].items():
        discount = (product['discount'] / 100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        sales_tax = ("%.2f" % (.09 * float(subtotal)))
        g_total = float("%.2f" % (float(sales_tax) + subtotal))

    return render_template('cart.html', g_total=g_total, sales_tax=sales_tax)


@app.route('/remove/<int:id>')
def remove(id):
    """
    lets user delete items from cart
    """
    if 'Cart' not in session or len(session['Cart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Cart'].items():
            if int(key) == id:
                session['Cart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception:

        return redirect(url_for('getCart'))


@app.route('/clear')
def clear():
    """
    Clears the current items in cart
    """
    session.pop('Cart', None)
    return redirect(url_for('home'))


@app.route('/signUp', methods=['GET', 'POST'])
def signup():
    """
    Manages the signup for Customer
    Retrives info from the signup form and adds it to the database
    """
    if not current_user.is_authenticated:
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
                db.session.commit()
                flash('Account created for user {}'.format(form.username.data))
            except Exception:
                flash('Username or email is taken')
                return redirect(url_for('signup'))
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))
    return render_template('signUp.html', title='Sign Up', form=form)


@app.route('/product/<product_id>', methods=['GET', 'POST'])
def productpage(product_id):
    product = AddProduct.query.get(product_id)
    reviews = product.reviews
    if 'Rate Product' in request.form:
        if current_user.is_authenticated:  # if user is logged in, route to review page, otherwise, route to login page
            return redirect(url_for('review', product_id=product_id))
        return redirect(url_for('login'))
    return render_template('items/productDetails.html', title='Product Details', product=product, reviews=reviews)


@app.route('/product/review/<product_id>', methods=['GET', 'POST'])
def review(product_id):
    product = AddProduct.query.get(product_id)
    if product == None:
        return redirect(url_for('home'))
    if current_user.is_authenticated:
        # if the cancel button is pressed, then route to the product page
        form = ReviewForm(request.form)
        if 'Cancel Review' in request.form:
            return redirect(url_for('productpage', product_id=product_id))
            # if a user is logged in and has selected a product to review, then the review is added
        if form.validate_on_submit():
            user = current_user
            reviewExists = False
            # get the old review object if it exists
            review = Review.query.filter(Review.username == user.username and Review.product_id == product_id).first()
            if review != None:
                reviewExists = True
            rating = form.rating.data
            reviewdata = form.review.data
            if rating <= 5 and rating >= 0:
                ## if there is no review, then add a review
                if reviewExists:
                    review.review = reviewdata
                    review.rating = rating
                    db.session.commit()
                    flash(f'Your review has been updated')
                else:
                    newreview = Review(username=user.username, rating=rating, review=reviewdata, product_id=product_id)
                    db.session.add(newreview)
                    db.session.commit()
                    flash(f'Your review has been added')
                return redirect(url_for('productpage', product_id=product_id))
            else:
                flash('Rating must be from 0-5 stars')
    else:
        return redirect(url_for('login'))
    return render_template('items/productReview.html', title='Product Review', form=form, product=product)


@app.route('/user/profile/username', methods=['GET', 'POST'])
def editusername():
    if current_user.is_authenticated:

        user = current_user
        form = EditUsernameForm(request.form)
        if form.validate_on_submit():
            new_username = form.username.data
            try:
                user.username = new_username
                db.session.commit()
                return redirect(url_for('userprofile'))
            except Exception:
                db.session.rollback()
                flash('The username is taken')
        if 'Cancel' in request.form:
            return redirect(url_for('userprofile'))
    else:
        return redirect(url_for('login'))
    return render_template('editUsername.html', title='Edit Username', form=form, user=user)


@app.route('/user/profile/email', methods=['GET', 'POST'])
def editemail():
    if current_user.is_authenticated:
        user = current_user
        form = EditEmailForm(request.form)
        if form.validate_on_submit():
            new_email = form.email.data
            try:
                user.email = new_email
                db.session.commit()
                return redirect(url_for('userprofile'))
            except Exception:
                db.session.rollback()
                flash('Email is already used')
        if 'Cancel' in request.form:
            return redirect(url_for('userprofile'))
    else:
        return redirect(url_for('login'))
    return render_template('editEmail.html', title='Edit Email', form=form, user=user)


@app.route('/user/profile/password', methods=['GET', 'POST'])
def editpassword():
    if current_user.is_authenticated:
        user = current_user
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
        return redirect(url_for('login'))
    return render_template('editPassword.html', title='Edit Password', form=form, user=user)


@app.route('/user/profile/address', methods=['GET', 'POST'])
def editaddress():
    if current_user.is_authenticated:
        user = current_user
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
        return redirect(url_for('login'))
    return render_template('editAddress.html', title='Edit Address', form=form, user=user)


@app.route('/user/profile', methods=['GET', 'POST'])
def userprofile():
    if current_user.is_authenticated:
        user = current_user
        if 'Edit Username' in request.form:
            return redirect(url_for('editusername'))
        if 'Edit Email' in request.form:
            return redirect(url_for('editemail'))
        if 'Edit Password' in request.form:
            return redirect(url_for('editpassword'))
        if 'Edit Address' in request.form:
            return redirect(url_for('editaddress'))
        if 'Delete Account' in request.form:
            return redirect(url_for('deleteaccount'))
    else:
        return redirect(url_for('login'))
    return render_template('userProfile.html', title='User Profile', user=user)


@app.route('/user/delete', methods=['GET', 'POST'])
def deleteaccount():
    if current_user.is_authenticated:
        user = current_user
        if 'Yes' in request.form:
            username = user.username
            db.session.delete(user)
            db.session.commit()
            flash('User {} has been deleted'.format(username))
            return redirect(url_for('home'))
        if 'No' in request.form:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
    return render_template('deleteAccount.html', title='Delete Account', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Manges the login for customer trying to login
    Checks for the password and retieve the user profile for right user
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    """
    Manges the logout response from user
    Securely logs out the customer and redirects them to login page
    """
    logout_user()
    return redirect(url_for('login'))


@app.route('/order')
@login_required
def order():
    """
    create order for checked out cart items
    """
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)

        order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['Cart'])
        db.session.add(order)
        db.session.commit()
        session.pop('Cart')
        return redirect(url_for('orders', invoice=invoice))


@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    """
       Order page display for checked out items in cart
    """
    if current_user.is_authenticated:
        grandTotal = 0
        subtotal = 0
        customer_id = current_user.id
        customer = User.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(
            CustomerOrder.id.desc()).first()
        for _key, product in orders.orders.items():
            discount = (product['discount'] / 100) * float(product['price'])
            subtotal += float(product['price']) * int(product['quantity'])
            subtotal -= discount
            sales_tax = ("%.2f" % (.09 * float(subtotal)))
            g_total = ("%.2f" % (float(sales_tax) + float(subtotal)))



    else:
        return redirect(url_for('customerLogin'))
    return render_template('orders.html', invoice=invoice, sales_tax=sales_tax, subtotal=subtotal, g_total=g_total,
                           customer=customer, orders=orders)
