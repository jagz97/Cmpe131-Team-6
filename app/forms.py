
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, SubmitField, StringField, IntegerField, TextAreaField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Products(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    discount = IntegerField('Discount')
    price = IntegerField('Price', validators=[DataRequired()])
    availableStock = IntegerField(
        'Available Stock', validators=[DataRequired()])
    submit = SubmitField('Submit')


    image = FileField('Image 1', validators=[
        FileRequired(), FileAllowed(['png', 'gif', 'jpg', 'jpeg'])])
    image_1 = FileField('Image 2', validators=[
                        FileRequired(), FileAllowed(['png', 'gif', 'jpg', 'jpeg'])])
    image_2 = FileField('Image 3', validators=[
                        FileRequired(), FileAllowed(['png', 'gif', 'jpg', 'jpeg'])])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    full_name = StringField('Full Name', validators=[DataRequired()])
    address_line_one = StringField('Address Line 1', validators=[DataRequired()])
    address_line_two = StringField('Address Line 2')
    city = StringField('City', validators=[DataRequired()])
    state_province_region = StringField('State/Province/Region', validators=[DataRequired()])
    zip_postal_code = IntegerField('ZIP/Postal Code', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Create Account')


class AddressForm(FlaskForm):
    full_name = StringField('Full Name',validators=[DataRequired()])
    address_line_one = StringField('Address Line 1',validators=[DataRequired()])
    address_line_two = StringField('Address Line 2')
    city = StringField('City',validators=[DataRequired()])
    state_province_region = StringField('State/Province/Region',validators=[DataRequired()])
    zip_postal_code = StringField('ZIP/Postal Code',validators=[DataRequired()])
    country = StringField('Country',validators=[DataRequired()])
    submit = SubmitField('Add Address')


class ReviewForm(FlaskForm):
    rating = IntegerField('# of Stars', validators=[DataRequired()])
    review = StringField('Enter review')
    submit = SubmitField('Add rating')


class EditUsernameForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Edit Username')


class EditEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Edit Email')


class EditPasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    confirm_current_password = PasswordField('Confirm Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Edit Password')

class MerchantSignup(FlaskForm):
    fullname = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    reenter = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField('Submit')

class MerchantLogin(FlaskForm):
    fullname = StringField('Name', validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')