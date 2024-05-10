from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FormField, Form, SelectField, HiddenField, FloatField, FieldList, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.widgets import NumberInput, HiddenInput, ListWidget, RadioInput, Select, TextInput, TableWidget
from models import AssessmentComponent, AssessmentStandard, AssessmentScore, StudentClassroomAssociation, Classroom
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
    component_id = HiddenField('Component ID')
    score = FloatField('Score', default=0.0, widget=NumberInput())


    

    # def __init__(self, obj=AssessmentComponent().id, *args, **kwargs):
    #     super(ComponentForm, self).__init__(*args, **kwargs)
    #     self.score.widget.input_type = 'number'
    #     self.score.widget.min = 0.0
    #     self.score.widget.max = 100.0
    #     self.score.widget.step = 1.0
    #     self.score.widget.value = 0.0
    #     self.score.label = 'Score'
    #     self.score.default = 0.0
    #     self.score.validators = [DataRequired()]
    #     self.score.render_kw = {'class': 'form-control', 'placeholder': 'Score'}
    #     self.component_id.label = 'Component ID'
    #     self.component_id.default = obj

class AssessmentScoreForm(FlaskForm):
    student_id = HiddenField('Student ID')
    assessment_name=HiddenField(u'Assessment Name')
    period = SelectField("Choose an option", validate_choice=False, choices={'1':'fall','2':'winter','3':'spring'}) 
    components = FieldList(FormField(ComponentForm))
    submit = SubmitField()

#new ideas: one - changing the field list to student id and iterating through components. two - changing the score field to a form field in assessment score form
# three  - try making a table widget for the component form (still don't)
# class ComponentScoreForm(FlaskForm):
#     component_id = HiddenField('Component ID')
#     score = FloatField('Score', default=0.0, widget=NumberInput())

