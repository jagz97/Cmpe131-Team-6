from app import app as app
from app import db, photos, search
from flask import render_template, redirect, url_for, request, flash, session
from app.forms import Products, SearchForm, MerchantSignup, MerchantLogin
from app.models import Brand, Category, AddProduct, Merchant
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
