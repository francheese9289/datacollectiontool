from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms import Form, StringField
from wtforms.widgets import TableWidget
from wtforms.fields import FieldList, FormField

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
    

        

class PARScoreForm(FlaskForm):
    '''Record or edit student assessment scores for PAR'''
    period = SelectField('Period', validators = [DataRequired()], choices = [('1','fall'), ('2', 'winter'), ('3','spring')])
    parlwss = IntegerField('Letter Word Calling', validators = [DataRequired()])
    parpn = IntegerField('Picture Naming', validators = [DataRequired()])
    parpa = IntegerField('Phonemic Awareness', validators = [DataRequired()])
    parrn = IntegerField('Rapid Naming', validators = [DataRequired()])
    partss = IntegerField('Total Standardized Score', validators = [DataRequired()])

#possible to make one form that pulls fields from a dictionary or queries assement table for option
#ex. subject>assessment_name>classroom(load students)>components
class ScoreForm(FlaskForm):
    Subject = SelectField('Subject', validators = [DataRequired()], choices = [('1','literacy'), ('2', 'math'), ('3','social emotional')])
    Period = SelectField('Period', validators = [DataRequired()], choices = [('1','fall'), ('2', 'winter'), ('3','spring')])


class PNOAScoreForm(ScoreForm):
    '''Record or edit student assessment scores for PNOA'''
    PNOAFS = IntegerField('Forward Sequence')
    PNOABS = IntegerField('Backward Sequence')
    PNOAEM = IntegerField('Symbolic Notation')
    PNOAOP = IntegerField('Operations')
    PNOAEQ = IntegerField('Equality')


class ScoringForm(FlaskForm):
    
    Period = SelectField('Period', validators = [DataRequired()], choices = [('1','fall'), ('2', 'winter'), ('3','spring')])
    # Classroom = SelectField('Class', choices = []) #still have to figure this one out

class PARTable(Form):
    fields = FieldList(FormField(PARScoreForm), widget=TableWidget())
    
