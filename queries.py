from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, HiddenField, SelectField, BooleanField, IntegerField, Form
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms.widgets import NumberInput, HiddenInput, TableWidget
from wtforms.fields import FieldList, FormField
from flask import request, flash, redirect, url_for, render_template
from app import db
from models import *
from flask_login import current_user





'''Working out how to create a form with a dynamic number of fields.'''

#Step One: Landing Page (or header) > User selects assessment and period
#Step Two: pull dict of components from chosen assessment and period

def component_dict(assessment, period, grade_level):
    '''Find all assesment ids for the assessment & recording period.'''
    assessment_components = db.session.scalars(sa.select(
        AssessmentStandard).where(
            sa.and_(AssessmentStandard.assessment_name==assessment, AssessmentStandard.period==period, AssessmentStandard.grade_level==grade_level)))
    #create a list of dicts with id, name, and period for each component
    data=[]
    for component in assessment_components:
            data.append({'id':component.id, 'name':component.component_name, 'period':component.period, 'grade_level':component.grade_level})
    return data



#Step Four: Create forms that capture the data for each student in a classroom and their current scores on the chosen assessment(& period).




#Step Three: Set up the data to populate form for each student.
# def new_assessment_grades(dict, roster, classroom):
#     '''
#     Set up the data to populate form. Scores are set to None. 
#     Function only called if there are no existing scores for the classroom/student.'''
#     data = {}
#     for student in roster:
#         for key, value in dict.items():
#             #creates data that can be mapped to the AssessmentScore object.
#             data={
#                 'student_score':None, 
#                 'assessment_id':db.session(sa.select(AssessmentStandard).where(AssessmentStandard.component_name == value['id'])),
#                 'student_id':student,
#                 'classroom_id':classroom,
#                 'period': value['period'],
#             }
        
#     return data