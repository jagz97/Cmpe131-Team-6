from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form,SubmitField, StringField, IntegerField,TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class Products(Form):
    name = StringField('Name',validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    discount = IntegerField('Discount')
    price = IntegerField('Price',validators=[DataRequired()])
    availableStock = IntegerField('Available Stock', validators=[DataRequired()])
    submit = SubmitField('Submit')

    image = FileField('Image 1', validators=[FileRequired(), FileAllowed(['png','gif','jpg','jpeg'])])
    image1 = FileField('Image 2', validators=[FileRequired(), FileAllowed(['png','gif','jpg','jpeg'])])
    image2 = FileField('Image 3', validators=[FileRequired(), FileAllowed(['png','gif','jpg','jpeg'])])
class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
class AddressForm(Form):
    full_name = StringField('Full Name',validators=[DataRequired()])
    address_line_one = StringField('Address Line 1',validators=[DataRequired()])
    address_line_two = StringField('Address Line 2')
    city = StringField('City',validators=[DataRequired()])
    state_province_region = StringField('State/Province/Region',validators=[DataRequired()])
    zip_postal_code = StringField('ZIP/Postal Code',validators=[DataRequired()])
    country = StringField('Country',validators=[DataRequired()])
    submit = SubmitField('Add Address')
