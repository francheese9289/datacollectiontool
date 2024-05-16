from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import current_user
from models import db, User, Staff, Student, AssessmentStandard, AssessmentComponent, AssessmentScore, StudentClassroomAssociation, Classroom
from forms import AssessmentScoreForm, ComponentForm, EditAssessmentScoreForm
import sqlalchemy as sa
import pandas as pd
import plotly.express as px

api = Blueprint('api',__name__, url_prefix='/api', template_folder='data_templates')


@api.route('/data_entry', methods=['GET', 'POST'])
def data_entry():
    user=current_user
    current_class = user.get_current_classroom()
    return render_template('data_entry.html')


@api.route('/data_entry/literacy', methods=['GET', 'POST'])
def data_entry_lit(): # <this will need to accept an assessment name (and subject?) as a parameter>

    #how do I disable options if scores already entered?? 

    #find current user and their most recent classroom
    assessment_name = 'Predictive Assessment of Reading' #drove myself fucking insane trying to make a dynamic route for assessments
    user=current_user
    current_class = user.get_current_classroom() #returns classroom object
    students = current_class.class_students
    roster_data = []
    for student in students:
        roster_data.append({
            'id': student.class_student.id,
            'full_name': student.class_student.full_name
        })
    
    #get all components for a given assessment 
    components = db.session.scalars(
        sa.select(AssessmentComponent).where(
            AssessmentComponent.assessment_name == assessment_name).order_by(
                AssessmentComponent.component_name)).all()
    #main form
    form = AssessmentScoreForm()
    #nested form
    component_form = ComponentForm()

    if form.validate_on_submit():
        period = request.form.get('period')
        
        for student_data in roster_data:
            student_id = student_data['id']
            
            for component in components:
                component_id = component.id
                
                # using html form to get the student's score
                score_key = f"score_{student_id}_{component_id}"
                #I THINK using 'request' allows for CSRF protection?
                student_score = request.form.get(score_key)
                
                # create a new score instance and populate its attributes
                new_score = AssessmentScore()
                new_score.period = period
                new_score.component_id = component_id
                new_score.student_id = student_id
                new_score.classroom_id = current_class.id
                new_score.student_score = student_score
                
                # add the score instance to the session
                db.session.add(new_score)
        db.session.commit()

        flash('Data entered successfully!', 'success')
        # Need to change this redirect to the dash or a data entry landing page
        return redirect(url_for('api.data_entry_lit'))

    return render_template('literacy.html', form=form, components=components, component_form=component_form, roster_data=roster_data)

@api.route('/data_entry/math', methods=['GET', 'POST'])
def data_entry_math(): 
    assessment_name = 'Primary Number & Operations Assessment' 
    user=current_user
    current_class = user.get_current_classroom() 
    students = current_class.class_students
    roster_data = []
    for student in students:
        roster_data.append({
            'id': student.class_student.id,
            'full_name': student.class_student.full_name
        })
    
    #get all components for a given assessment 
    components = db.session.scalars(
        sa.select(AssessmentComponent).where(
            AssessmentComponent.assessment_name == assessment_name).order_by(
                AssessmentComponent.component_name)).all()
    #main form
    form = AssessmentScoreForm()
    #nested form
    component_form = ComponentForm()
    
    for component in components:
        component_form.component_id = component.id
        form.components.append_entry(component_form) #DELETE THIS NOW???

    if form.validate_on_submit():
        period = request.form.get('period')
        
        for student_data in roster_data:
            student_id = student_data['id']
            
            for component in components:
                component_id = component.id
                
                # using html form to get the student's score
                score_key = f"score_{student_id}_{component_id}"
                #I THINK using 'request' allows for CSRF protection?
                student_score = request.form.get(score_key)
                
                # create a new score instance and populate its attributes
                new_score = AssessmentScore()
                new_score.period = period
                new_score.component_id = component_id
                new_score.student_id = student_id
                new_score.classroom_id = current_class.id
                new_score.student_score = student_score
                
                # add the score instance to the session
                db.session.add(new_score)
        db.session.commit()

        flash('Data entered successfully!', 'success')
        return redirect(url_for('api.index'))

    return render_template('math.html', assessment_name=assessment_name, form=form, components=components, component_form=component_form, roster_data=roster_data)

# @api.route('/data_entry/edit', methods=['GET','POST'])
# def data_entry_edit():
