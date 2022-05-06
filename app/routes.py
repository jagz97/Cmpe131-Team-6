from app import app as app
from app import db, photos, search
from unicodedata import category
from flask import render_template, redirect, url_for, request, flash, session, current_app
from app.forms import Products, LoginForm, SignUpForm, ReviewForm, EditUsernameForm, EditPasswordForm, EditEmailForm, AddressForm, SearchForm, MerchantSignup, MerchantLogin
from app.models import Brand, Category, AddProduct, User, Review, Merchant
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import update
from flask_wtf import FlaskForm
from wtforms import StringField
from app.helpers import seller_required
from werkzeug.security import check_password_hash, generate_password_hash

@app.route('/')
def home():
    products = AddProduct.query.filter(AddProduct.availablestock > 0)

    return render_template('home.html', products=products)

@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = AddProduct.query.msearch(searchword, fields=['name','description'] , limit=3)
    
    return render_template('search.html',products= products)

@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
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
                             description=description, availablestock=availablestock, image=image, image_1=image_1, image_2=image_2,username= session['username'])

        db.session.add(addprod)
        # if form is successfully submitted show success message
        flash(f'Product {form.name.data} has been added')
        db.session.commit()
        rows = AddProduct.query.filter_by(username=session['username'])
        return render_template('items/product.html', title='title', form=form, brands=brands, categories=categories, rows = rows )
    rows = AddProduct.query.filter_by(username=session['username'])
    return render_template('items/product.html', title='title', form=form, brands=brands, categories=categories, rows = rows)


#merchant signup
@app.route('/signupmerchant',  methods=['GET', 'POST'])
def signup_merchant():
    form = MerchantSignup(request.form)
    if request.method== "POST":
        session.clear()
        password = form.password.data
        reenter = form.reenter.data
        if(password!=reenter):
            flash('Passwords do not match')
            return redirect(url_for('signup_merchant'))

        #passwordHash
        pass_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        fullname = form.fullname.data
        username = form.username.data

        #db store
        new_usr = Merchant(fullname = fullname, username=username,password=pass_hash)
        try:
            db.session.add(new_usr)
            db.session.commit()
        except:
            flash('User Name already taken')
            return redirect(url_for('signup_merchant'))
        return redirect(url_for('login_merchant'))
        
    return render_template("merchantsignup.html",form= form)


@app.route('/merchantlogin', methods=['GET','POST'])
def login_merchant():
    form = MerchantLogin(request.form)
    if request.method=='POST':
        session.clear()
        username = form.fullname.data
        password = form.password.data
        result = Merchant.query.filter_by(username=username).first()
        # checking if username exist and password entered it correct
        if result == None or not check_password_hash(result.password, password):
            flash('Username or Password Incorrect. Please try again')
            return redirect(url_for('login_merchant'))
    
         #remember the logged in user
        session["username"] = result.username
        return redirect(url_for('addproduct') )
    return render_template('merchantlogin.html', form = form)

  
@app.route('/merchantlogout')
def logut_merchant():
    session.clear()
    flash('You have been logged out.Login again?')
    return redirect(url_for('login_merchant'))

  
@app.route('/addcart', methods=['POST','GET'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        product = AddProduct.query.filter_by(id=product_id).first()
        if product_id and request.method == "POST":
            ditems = {product_id:{'name':product.name,'price':product.price,'discount':product.discount,'image':product.image}}
        if 'Cart' in session:
            print(session['Cart'])
            if product_id in session['Cart']:
               flash("Item already in cart")
            else:
                session['Cart']= Merge(session['Cart'],ditems)
                return redirect(request.referrer)
        else:
            session['Cart']= ditems
            return redirect(request.referrer)   
    except Exception as e:
        flash("Failed, Please try again")
    finally:
        return redirect(request.referrer)

def Merge(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


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
                flash('Username or email is taken')
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
    if 'Rate Product' in request.form:
        session['product_id'] = product_id
        if 'id' in session:# if user is logged in, route to review page, otherwise, route to login page
            return redirect(url_for('review'))
        session.pop('product_id', None)
        return redirect(url_for('home'))
    return render_template('items/productDetails.html', title='Product Details', product=product)


@app.route('/product/review', methods=['GET', 'POST'])
def review():
    if 'id' in session and session['id'] != None and 'product_id' in session and session['product_id'] != None:
        # if the cancel button is pressed, then route to the product page
        form = ReviewForm(request.form)
        if 'Cancel Review' in request.form:
            product_id = session['product_id']
            session.pop('product_id', None)
            return redirect(url_for(productpage, product_id))
            # if a user is logged in and has selected a product to review, then the review is added
        if form.validate_on_submit():
            product_id = session['product_id']
            username = session['username']
            reviewExists = False
            # get the old review object if it exists
            review = Review.query.filter(Review.username == username).first()
            if review != None:
                reviewExists = True
            rating = form.rating.data
            reviewdata = form.review.data
            ## if there is no review, then add a review
            if not reviewExists:
                newreview = Review(username=username, rating=rating, review=reviewdata, product_id=product_id)
                db.session.add(newreview)
                db.session.commit()
                flash(f'Your review has been added')
            # else update the old review
            #else:
                #review.review =
            url = '/product/' + product_id
            session.pop('product_id', None)
            return redirect(url_for(url))
        else: # the product or the user is not in session, so the page is rerouted to the home page
            return redirect(url_for(''))
    else:
        return redirect(url_for('home'))
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
        if 'Delete Account' in request.form:
            return redirect(url_for('deleteaccount'))
    else:
        return redirect(url_for('home'))
    return render_template('userProfile.html', title='User Profile', user=user)


@app.route('/user/delete', methods=['GET', 'POST'])
def deleteaccount():
    if 'id' in session and session['id'] != None:
        user_id = session['id']
        user = User.query.get(user_id)
        if 'Yes' in request.form:
            username = user.username
            db.session.delete(user)
            db.session.commit()
            session.pop('id', None)
            session.pop('username', None)
            session.pop('email', None)
            flash('User {} has been deleted'.format(username))
            return redirect(url_for('home'))
        if 'No' in request.form:
            return redirect(url_for('userprofile'))
    else:
        return redirect(url_for('home'))
    return render_template('deleteAccount.html', title='Delete Account', user=user)
