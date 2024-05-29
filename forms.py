from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField, BooleanField, FormField, Form, SelectField, HiddenField, FloatField, FieldList
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.widgets import NumberInput
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
    submit = SubmitField()

#Nested Form
class ComponentForm(Form):
    component_id = HiddenField('Component ID')
    score = FloatField('Score', default=0.0, widget=NumberInput())

#Main Form
class AssessmentScoreForm(FlaskForm):
    student_id = HiddenField('Student ID')
    assessment_name=HiddenField(u'Assessment Name')
    period = SelectField("Choose an option", validate_choice=False, choices={'1':'fall','2':'winter','3':'spring'}) 
    components = FieldList(FormField(ComponentForm))
    submit = SubmitField()

class EditAssessmentScoreForm(FlaskForm):
    student_id = HiddenField('Student ID')
    assessment_name=HiddenField(u'Assessment Name')
    period = SelectField("Choose an option", validate_choice=False, choices={'1':'fall','2':'winter','3':'spring'}) 
    components = FieldList(FormField(ComponentForm))
    submit = SubmitField()