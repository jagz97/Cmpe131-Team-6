# Amazin
Webapp designed for merchants and buyers, a match made where both can buy and sell items. 
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [VENV Setup](#using-virtual-environment-is-recommended)
* [Setup and Run Application](#setup)
* [Navigation](#how-to-use)
* [Features](#features)
* [Credits](#cmpe131-team-6)

## General info
This webapp has been created/developed by students of SJSU as a part of class project for CMPE-131.

## Technologies
Project is created with:
* Flask version: 2.0.3
* Python version: 3.9.12
* Flask-Login
* Flask-msearch
* Flask-WTF
* SQLAlchemy
* Flask-Reuploaded
* Bootstraps
* CSS

## Setup
- Prerequisites: Python 3
    Python installation: [https://www.python.org/downloads/](https://www.python.org/downloads/)

To run this project, install it locally using terminal with these commands:

    $ git clone https://github.com/jagz97/Cmpe131-Team-6
    $ cd Cmpe131-Team-6
To install all required dependencies, type this command inside the project directory:

### Using virtual Environment is Recommended:
On terminal after sucessfully cloning the repository navigate to the project directory:
- Make virtual environment using python3:

```linux
$ python3 -m venv venv
```  
    

- Activate the virtual environment:
```linux
$ . venv/bin/activate
```

- Install all the required dependencies:

```
$ pip install -r requirements.txt
```
    

### How to Run
- Navigate to the project directory. 
- Type this command into your terminal:
``` 
$ python3 run.py
```
- Once the app starts running, it can be accessed from the local host which is available at url for local host http://127.0.0.1:5000/

## How to Use

### Splash Landing Page
- Lets users sign up for and receive newsletter using mailgun API. In order to facilitate this function was created using [MailgunAPI](https://documentation.mailgun.com/en/latest/):
```python
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
```

#### Home
- The home page is accessed through the local host post:5000 url http://127.0.0.1:5000/home
- The customer sign up page can be accessed through the `/register` link.
- The customer login page can be accessed through the `/login` link.
- The merchant login/sign up page can be accessed through the "Sign Up/Login Here" link.
- The user profile page can be accessed through the "Profile" link.
- A list of items will be displayed on the home page, and users can add to cart or access the product details page.
- Avaiable items can be viewed the home page and can be added to cart for checkout later.

#### Merchant 
* Merchant registation page can be accessed at `/signupmerchant` where merchants can create account and become seller.
   * Succesfull signup will take merchant to `/merchantlogin` page from where merchants can access their personalized products items where they can see thier added products and keep track of items left in stock.
   * Merchants can add a new product to the store from the `/addproduct` home page which allows merchants to add pictures for thier product.
   * Links to `/addcategoty` and `/addbrand` is included on `/addproduct` form page to add more categories and brands, if it doesn't exist.
*  Route `/addproduct` is protected page which is personalized merchant page. In order to prevent Users from accessing this page using a helper decorator function shown below sourced from flask documentation [View Decorators](https://flask.palletsprojects.com/en/2.1.x/patterns/viewdecorators/):

```python
def seller_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function
````
#### Search
* Search bar located on the navbar has the functionality to search for added items by keyword.
* Search functionality has been facilitated using the Flask dependancy msearch [documentation for flask-msearch](https://pypi.org/project/flask-msearch/):
In termianl:
```
pip install flask-msearch
```
In  `__init.py__` file initialize search to use functionality of msearch:
```python
search = Search()
search.init_app(app)
```
#### Cart
* Items can be added to cart from the home page without signup/login for customers.
* Customers can add items to cart from the home page. Each item has Add to Cart button which adds item to cart.
* Added items to cart can be viewed from `/cart` located on navbar. Empty cart cannot be accessed and reroutes back to the homepage.
* The cart items that are displayed in cart is jsonified data that was converted from slqlite to json format using:

Jsonify Slqlite Db Example:

 In `models.py`:
 ```python
 import json
 ```
 create class in `models.py`:
```python
class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)
```
* The cart items can be checked out using Fake Credit Card entry facilitated by using function from [StripeAPI](https://stripe.com/docs) documentation:
```python
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
```


#### Customer Login
- The user enters their username, password, and can choose to have the website remember them.
#### Create Customer Account
- The user enters their username, email, password, and address information.
#### Edit Customer Profile
- The user can view their profile and click on a button to choose the variable they want to edit
- The user can go to the delete account page through the "Delete Account" button
#### Delete Customer Account
- The user confirms the deletion or cancels the deletion with buttons.
#### Product Details + Reviews
- The user can view the reviews of a product and add a review with the button.
- The user will enter their star rating and can add a review if they like.

## Features

- Merchants can signup at `/signupmerchant` and login/logout at `/merchantlogin` `/merchantlogout` (Jagjit Singh)
- Merchants can add items to seller and view their added products at `/addproduct` (Jagjit Singh)
- Merchants can add pictures for product at `/addproduct` form and items are posted with pictures at `/` home (Jagjit Singh)
- Merchants can add items to bid with a starting bid price and must add pictures when adding the item at `/addbiddableitem` (Nicholas Bao)
- Customers can search for items from navbar search located at `/` home (Jagjit Singh)
- Customers can add items to cart from home `/` and view cart items added in cart at `/cart' (Jagjit Singh)
- Customers can  login at `/login` logout at`/logout` (Jagjit Singh)
- Customers can create customer account is at /signUp (Hector Saldivar)
- Customers can edit account at /user/profile, and bootstrap is added (Hector Saldivar)
- Customers can delete account at in a bootstrap modal within /user/profile (Hector Saldivar)
- Customers can view a products reviews and other details at /product/<product_id> (Hector Saldivar)
- Customers can add a review if they are logged in at /product/<product_id> through a button that brings up a modal (Hector Saldivar)
- Customers can check out the items in cart and buy items using Stripe API `orders/<order_id>` (Jagjit Singh)
- Users Land on Splash at `/` where they can signup to subscribe for newsletter using MailGun api (Jagjit Singh)
- Customer can see all items added by all sellers at `/home` (Jagjit Singh)
  - Bootstrap, CSS on splash page`/`, homepage `/home`, merchant, cart (Jagjit Singh)

# Cmpe131 Team 6
- Hector Saldivar (@HectorSal) Team Lead
- Jagjit Singh (@jagz97)
- Nicholas Bao (@nick55808)




