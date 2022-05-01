from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form,SubmitField, StringField, IntegerField,TextAreaField
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