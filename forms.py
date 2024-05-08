from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FormField, Form, SelectField, HiddenField, FloatField, FieldList, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.widgets import NumberInput, HiddenInput, ListWidget, RadioInput, Select

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

class ComponentForm(Form):
    component = HiddenField('Component', widget=HiddenInput())
    score = FloatField('Score', default=0.0, widget=NumberInput())

class AssessmentScoreForm(FlaskForm):
    student = StringField(u'Student Name') 
    components = FieldList(FormField(ComponentForm), min_entries=1, widget=ListWidget())



class ScoreParentData(FlaskForm):
    period = SelectField("Choose an option", validate_choice=False, choices=['fall','winter','spring']) 
    classroom = HiddenField(u'Classroom')
    assessment_name=SelectField("Choose an option", validate_choice=False, choices=['Predictive Assessment of Reading', 'Primary Number Operations Assessment'], widget=Select())
