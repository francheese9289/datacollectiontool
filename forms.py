from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo
from models import Staff, User, db, ma


class UserLoginForm(FlaskForm):
    email = StringField('Email', validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired()])
    submit_button = SubmitField()

class CheckUserForm(FlaskForm): 
    email = StringField('Email', validators=[Email()])

class UserSignUpForm(FlaskForm):
    first_name = StringField('First Name', validators = [InputRequired()])
    last_name = StringField('Last Name', validators = [InputRequired()])
    email = StringField('Email', validators = [InputRequired(), Email()]) 
    # username = StringField('Username', validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired()])
    confirm_password = PasswordField('Confirm Password', 
        validators=[InputRequired(), EqualTo('password', message='Passwords Must Match')])
    submit_button = SubmitField()

    def validate_staff_user(form, field):
        staff_member = Staff.query.filter_by(email = field.data).first()
        if staff_member:
           db.session.add(User.assigned_classrooms(staff_member))
           db.session.add(User.assigned_schools(staff_member))
        
            