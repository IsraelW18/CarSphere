from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=150)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=150)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class AddCarForm(FlaskForm):
    make = StringField('Make', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    year = SelectField('Year', validators=[DataRequired()])
    director = StringField('Director', validators=[DataRequired()])
    main_settings = StringField('Main Settings', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image_file = FileField('Car Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')])
    submit = SubmitField('Add Car to Gallery')


class ReviewForm(FlaskForm):
    review = TextAreaField("Let us know what's on your mind", validators=[DataRequired()])
    submit = SubmitField('Submit Review')