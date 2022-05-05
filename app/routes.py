from app import app as app
from app import db, photos, search
from flask import render_template, redirect, url_for, request, flash, request, session, current_app
from app.forms import Products, SearchForm
from app.models import Brand, Category, AddProduct
from flask_wtf import FlaskForm
from wtforms import StringField


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
                             description=description, availablestock=availablestock, image=image, image_1=image_1, image_2=image_2)

        db.session.add(addprod)
        # if form is successfully submitted show success message
        flash(f'Product {form.name.data} has been added')
        db.session.commit()
        return redirect(url_for('addproduct'))

    return render_template('items/product.html', title='title', form=form, brands=brands, categories=categories)


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
