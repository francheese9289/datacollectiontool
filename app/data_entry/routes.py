import sqlalchemy as sa
from flask import render_template, Blueprint, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired
from wtforms.widgets import TableWidget, HiddenInput
from models import User, Staff, Student, AssessmentScore, AssessmentStandard, StudentClassroomAssociation, db
from forms import StudentScoreForm, StudentForm
from flask_login import current_user
from werkzeug.datastructures import MultiDict
from collections import namedtuple

data = Blueprint('data', __name__, template_folder='data_templates')



#data/routes.py
@data.route('/data_entry/<assessment>', methods=['GET', 'POST'])
def data_entry(assessment):
 
    user = current_user
    staff = db.session.scalar(sa.select(Staff).where(Staff.id == user.staff_id))
    current_class = staff.staff_classrooms[-1]
    students = current_class.class_students
    assessment = assessment.replace('+',' ')

    form = StudentScoreForm()
    if assessment == 'Predictive Assessment of Reading':
        components = ['Letter Word Calling','Phonemic Awareness','Rapid Naming', 'Total Standardized Score','Picture Naming']
    else:
        components = AssessmentStandard.get_assessment_components(assessment=assessment)
    student_list=[]
    component_list=[]
    for student in students:
        for component in components:
            student_list.append(student)
            component_list.append(component)

    student_components = list(zip(student_list, component_list))
    ##testing importing info to dashboard
    return student_components







#    form = data_forms(assessment)
#     if form.validate_on_submit():
#         print('yes')

#         score_entry = AssessmentScore(
#             student_score=form.score.data,
#             assessment_id=form.assessments.data,
#             student_id=form.students.data,
#             classroom_id=current_class.id,
#             period=form.period.data
#         )
#         db.session.add(score_entry)
#     db.session.commit()

 
    
        
    # for student in students: 
    #     for component in components:
    #         print (component)
    #         #one form per student & component
    #         form = StudentScoreForm(assessment_id=component, classroom_id=current_class, student_id=student.class_student.id)
    #         scores.append(form)
    #         for form in scores:
    #             if form.validate_on_submit():
                   

    # # Render the template with the form object and other data
    # return render_template('literacy.html', form=form, scores=scores, students=students, components=components, assessment=assessment, classroom=current_class)
