from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
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

class PARScoreForm(FlaskForm):
    '''Record or edit student assessment scores for PAR'''
    Period = SelectField('Period', validators = [DataRequired()], choices = [('1','fall'), ('2', 'winter'), ('3','spring')])
    PARLWSS = IntegerField('Letter Word Calling', validators = [DataRequired()])
    PARPN = IntegerField('Picture Naming', validators = [DataRequired()])
    PARPA = IntegerField('Phonemic Awareness', validators = [DataRequired()])
    PARRN = IntegerField('Rapid Naming', validators = [DataRequired()])
    PARTSS = IntegerField('Total Standardized Score', validators = [DataRequired()])

#possible to make one form that pulls fields from a dictionary or queries assement table for option
#ex. subject>assessment_name>classroom(load students)>components

class PNOAScoreForm(FlaskForm):
    '''Record or edit student assessment scores for PNOA'''
    Period = SelectField('Period', validators = [DataRequired()], choices = [('1','fall'), ('2', 'winter'), ('3','spring')])
    PNOAFS = IntegerField('Forward Sequence')
    PNOABS = IntegerField('Backward Sequence')
    PNOAEM = IntegerField('Symbolic Notation')
    PNOAOP = IntegerField('Operations')
    PNOAEQ = IntegerField('Equality')


class ScoringForm(FlaskForm):
    Subject = SelectField('Subject', validators = [DataRequired()], choices = [('1','literacy'), ('2', 'math'), ('3','social emotional')])
    Period = SelectField('Period', validators = [DataRequired()], choices = [('1','fall'), ('2', 'winter'), ('3','spring')])
    # Classroom = SelectField('Class', choices = []) #still have to figure this one out