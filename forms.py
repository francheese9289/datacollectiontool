from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, HiddenField, SelectField, BooleanField, IntegerField, Form
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms.widgets import NumberInput, HiddenInput, TableWidget
from wtforms.fields import FieldList, FormField
from app import db
from models import *
from flask_login import current_user

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email(message='enter a valid email')])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField()

class UserRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators = [DataRequired()])
    last_name = StringField('Last Name', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()]) 
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
        validators=[DataRequired(), EqualTo('password', message='Passwords Must Match')])
    
#use FORM instead of FlaskForm when form is to be embedded into flask form

#forms.py
class StudentForm(Form):
    student_id = IntegerField('Student ID', validators = [DataRequired()])
    student_name = StringField('Student Name', validators = [DataRequired()])
    assessment_id = IntegerField('Assessment ID', validators = [DataRequired()])

class StudentScoreForm(FlaskForm):
    classroom_id = HiddenField('Classroom')
    period = SelectField('Period', validators = [DataRequired()], choices = [('1','fall'), ('2', 'winter'), ('3','spring')])
    score = FloatField('Score', validators=[DataRequired()])
    student_assessments = FieldList(FormField(StudentForm), min_entries=5)



