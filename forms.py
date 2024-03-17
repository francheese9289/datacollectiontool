from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class UserLoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email(message='enter a valid email')])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField()

class UserRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators = [DataRequired()])
    last_name = StringField('Last Name', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()]) 
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
        validators=[DataRequired(), EqualTo('password', message='Passwords Must Match')])

class PARDataEntry(FlaskForm):
    #is there where I would loop student names?