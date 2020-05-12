from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import Form, BooleanField, PasswordField
from wtforms import TextField, TextAreaField, SelectField, DateField, SelectMultipleField
from wtforms import validators, ValidationError
from wtforms.validators import DataRequired

##query- search
class QueryFormStructure(FlaskForm):
    LOCATION = SelectField('LOCATION:  ' , validators = [DataRequired()])
    submit = SubmitField('Confirm')

    #name   = StringField('Country Name:  ' , validators = [DataRequired()])
    #submit = SubmitField('Submit')
    #LOCATION = TextField("LOCATION",[validators.Required("Please enter a location.")])

##login
class LoginFormStructure(FlaskForm):
    username   = StringField('User name:  ' , validators = [DataRequired()])
    password   = PasswordField('Pass word:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')

##register
class UserRegistrationFormStructure(FlaskForm):
    FirstName  = StringField('First name:  ' , validators = [DataRequired()])
    LastName   = StringField('Last name:  ' , validators = [DataRequired()])
    PhoneNum   = StringField('Phone number:  ' , validators = [DataRequired()])
    EmailAddr  = StringField('E-Mail:  ' , validators = [DataRequired()])
    username   = StringField('User name:  ' , validators = [DataRequired()])
    password   = PasswordField('Pass word:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')
