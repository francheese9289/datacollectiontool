from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import current_user
from models import db, User, Staff, Student, AssessmentStandard, AssessmentScore, StudentClassroomAssociation
from forms import AssessmentScoreForm, ComponentForm, ScoreParentData
import sqlalchemy as sa

api = Blueprint('api',__name__, url_prefix='/api', template_folder='data_templates')

@api.route('/enter_data', methods=['GET', 'POST'])
def enter_data():
    '''landing page to gather correct assessment data'''
    user=current_user
    staff = db.session.scalar(sa.select(Staff).where(Staff.id == user.staff_id))
    current_class = staff.staff_classrooms[-1]
    
    grade_level = current_class.grade_level
    
    
    form = ScoreParentData()
    if request.method == 'POST' and form.validate():
        parent_data = {
            'period': form.period.data,
            'classroom_id': current_class.id,
            'assessment_name': form.assessment_name.data,
            'grade_level': grade_level
        }
        return redirect(url_for('api.enter_assessment_data', period=parent_data['period'], classroom_id=parent_data['classroom_id'], assessment_name=parent_data['assessment_name'], grade_level=parent_data['grade_level']))
    
    return render_template('enter_data.html', form=form)

@api.route('/enter_assessment_data/', methods=['GET', 'POST'])
def enter_assessment_data():
    period = request.args.get('period')
    current_class = request.args.get('classroom_id')
    assessment_name = request.args.get('assessment_name')
    grade_level = request.args.get('grade_level')
    students = db.session.scalars(sa.select(StudentClassroomAssociation.student_id).where(StudentClassroomAssociation.classroom_id == current_class))

    components = ['Letter Word Calling','Phonemic Awareness','Picture Naming','Rapid Naming','Total Standardized Score']
    
    form=AssessmentScoreForm()

    for component in components:
        #Need to pull unique component_name 
        form.components.append_entry(component)

    if request.method == 'POST' and form.validate():
        #create score instance and set period, student_id, classroom_id
        for student in students:
            print (student)
            new_score = AssessmentScore()
            new_score.student_id = student.id
            new_score.classroom_id = current_class       
            new_score.student_score = form.components.score
            db.session.add(new_score)
            
        db.session.commit()
        flash('Data entered successfully!','success')
        return redirect(url_for('api.enter_data'))
    else:
        if request.method == 'POST':
            print('NOT VALID DUMDUM')
    return render_template('comp_form.html', form=form, students=students, components=components)


def get_assessment_id(assessment, grade_level, period):
    comps = db.session.scalars(sa.select(AssessmentStandard).where(sa.and_(AssessmentStandard.assessment_name == assessment, AssessmentStandard.grade_level == grade_level, AssessmentStandard.period == period))).all()
    return comps if comps is not None else []

