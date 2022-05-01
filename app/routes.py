from unicodedata import category
from flask import render_template,redirect, url_for,request,flash
from app.forms import Products
from app.models import Brand, Category
from app import app,db
from flask_wtf import FlaskForm
from wtforms import StringField

brands = Brand.query.all()
category = Category.query.all() 

@app.route('/')
def home():
    title = "HomePage"
    return render_template('base.html', title=title)

@app.route('/addbrand', methods=['GET','POST'])
def addbrand():
    if request.method=="POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The brand {getbrand} has been added','success')
        db.session.commit()
        return redirect(url_for('addbrand'))
        
    return render_template('items/brand.html', brand = 'brand')

@app.route('/addcategory', methods=['GET','POST'])
def addcategory():
    if request.method=="POST":
        getcat = request.form.get('category')
        category= Category(name=getcat)
        db.session.add(category)
        flash(f'The category {getcat} has been added','success')
        db.session.commit()
        return redirect(url_for('addbrand'))
        
    return render_template('items/brand.html')




@app.route('/addproduct', methods=['GET','POST'])

      
def addproduct():
    brands = Brand.query.all()
    category = Category.query.all() 
    form = Products(request.form)
    if request.method=='POST':
        flash(f'Product {form.name.data} has been added')
        return redirect(url_for('addproduct'))
           
    
    return render_template('items/product.html', title='title', form = form,brands = brands , category = category)
