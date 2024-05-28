import sqlalchemy as sa
import numpy as np
from flask import request, jsonify, render_template, redirect, url_for, flash
from flask_login import current_user
from models import db, AssessmentComponent, AssessmentScore, Classroom
from forms import AssessmentScoreForm, ComponentForm, EditAssessmentScoreForm
from app.services.data_analysis import *
from app.api.routes import *
from psycopg2.extensions import register_adapter, AsIs
register_adapter(np.int32, AsIs)
register_adapter(np.int64, AsIs)

def render_data_entry_parameters():
    user=current_user
    current_class = user.get_current_classroom() 
    assessments = current_class.get_grade_level_assessments()
    periods = {1:'fall', 2:'winter', 3:'spring'}
    return render_template('data_entry_params.html', assessments=assessments, periods=periods)

def process_data_entry_parameters():
    assessment = request.form.get('assessment')
    period = request.form.get('period')
    if assessment and period:
        return redirect(url_for('api.data_entry', assessment_name=assessment, period=period))
    else:
        flash('Please select both an assessment and a period', 'error')
        return redirect(url_for('api.data_entry_params'))


def render_data_entry_template(assessment_name, period):
    """Render data entry template."""
    user=current_user

    current_class = user.get_current_classroom() 
    roster_data = current_class.classroom_roster()
    components = AssessmentComponent.query.filter_by(assessment_name=assessment_name).order_by(
        AssessmentComponent.component_name).all()
    form = AssessmentScoreForm()
    
    return render_template('data_entry.html', form=form, components=components, assessment_name=assessment_name, roster_data=roster_data)


def process_data_entry_request(assessment_name, period):
    """Process data entry request."""
    user=current_user

    current_class = user.get_current_classroom() 
    roster_data = current_class.classroom_roster()

    components = db.session.scalars(
        sa.select(AssessmentComponent).where(
            AssessmentComponent.assessment_name == assessment_name).order_by(
                AssessmentComponent.component_name)).all()
    
    #main form
    form = AssessmentScoreForm()
    #nested form
    component_form = ComponentForm()

    if request.method == 'POST':
        form = AssessmentScoreForm(request.form)
        if form.validate():
        
            for student_data in roster_data:
                student_id = student_data['student_id']
                
                for component in components:
                    component_id = component.id
                    
                    # using html form to get the student's score
                    score_key = f"score_{student_id}_{component_id}"
                    student_score = request.form.get(score_key)
                    
                    # create a new score instance and populate its attributes
                    new_score = AssessmentScore()
                    new_score.period = period
                    new_score.component_id = component_id
                    new_score.student_id = student_id
                    new_score.classroom_id = current_class.id
                    new_score.student_score = student_score
                    new_score.class_assessment_id = new_score.class_assessment_id()
                    # add the score instance to the session
                    db.session.add(new_score)
                    db.session.commit()
            if not form.validate_on_submit():
                flash('Error processing form submission', 'error')
                return redirect(url_for('api.edit_data'))
            return jsonify({'message': 'Data entry successful'}), 201
        else:
            return jsonify({'error': 'Form validation failed'}), 400
    else:
        return jsonify({'error': 'Method not allowed'}), 405




def render_edit_data_template(assessment_name, period):
    user = current_user
    current_class = user.get_current_classroom()
    roster_data = current_class.classroom_roster()
    
    components = AssessmentComponent.query.filter_by(assessment_name=assessment_name).order_by(
        AssessmentComponent.component_name).all()
    class_score_data = get_data(current_class.id)

    filtered_score_data = class_score_data.loc[(class_score_data['assessment_name'] == assessment_name) & (class_score_data['period'] == period)]
    
    data = {}  # dict for pertinent student score data needed to populate form
    for _, row in filtered_score_data.iterrows():  # underscore used to ignore index in loop!
        student = row['student']  # student_name
        print(student)
        if student not in data:
            data[student] = {'scores': []}  # list of scores for given assessment
        data[student]['scores'].append({
            'component_id': row['component_id'],
            'score_id': row['score_id'],
            'score_value': row['student_score']
        })

    form = EditAssessmentScoreForm()
    
    return render_template('edit_data.html', form=form, components=components, assessment_name=assessment_name, period=period, roster_data=roster_data, data=data)



def process_edit_data_request(assessment_name, period):
    user = current_user
    current_class = user.get_current_classroom()
    class_score_data = get_data(current_class.id)
    
    filtered_score_data = class_score_data[(class_score_data['period'] == int(period)) & (class_score_data['assessment_name'] == assessment_name)]
    
    
    if filtered_score_data.empty: #this doesnt work
        flash('No data entered for selected assessment and period', 'error')
        return redirect(url_for('api.edit_data_params'))  # Redirect to the edit data page

    components = filtered_score_data[['component_id', 'component_name']].drop_duplicates().sort_values('component_name').to_dict('records')
    data = {}  # dict for pertinent student score data needed to populate form
    for _, row in filtered_score_data.iterrows():  # underscore used to ignore index in loop!
        student = row['student']  # student_name
        if student not in data:
            data[student] = {'scores': []}  # list of scores for given assessment
        data[student]['scores'].append({
            'component_id': row['component_id'],
            'score_id': row['score_id'],
            'score_value': row['student_score']
        })

    form = EditAssessmentScoreForm()

    if form.validate_on_submit():
        all_valid = True  # flag to check if all updates are valid
        for student, student_data in data.items():
            for score_data in student_data['scores']:
                score_id = score_data['score_id']
                student_score = request.form.get(f'student_score_{score_id}')

                if score_id and student_score is not None:
                    try:
                        update_score = db.session.query(AssessmentScore).get(score_id)
                        if update_score:
                            update_score.period = period
                            update_score.student_score = float(student_score)
                    except Exception as e:
                        all_valid = False
                        flash(f"Error updating score for student {student}: {e}", 'error')

        if all_valid:
            db.session.commit()
            flash('Scores successfully updated!', 'success')
            return redirect(url_for('api.edit_data', assessment_name=assessment_name, period=period))
        else:
            db.session.rollback()  # rollback if any errors occurred
            flash('Failed to update scores. Please try again.', 'error')
            
    return render_template('edit_data.html', form=form, data=data, components=components, assessment_name=assessment_name, period=period)


# def make_something(class_id):
#     classroom = db.session.scalar(sa.select(Classroom).where(Classroom.id == class_id))
#     class_scores = classroom.class_scores
#     comp_score_dict ={}
#     i=0
#     for score in class_scores:
#         comp_score_dict[score.period]={
#             'component': score.component_id,
#             'scores': [s for s in score.student_score],
#             ''
#         }
        


# def class_percentiles(class_id, subject): 
#     data = get_data(class_id)
#     #create new list of dicts with subject specific scores
#     new_data=[]
#     for datum in data:
#         filtered_dict = {k:v for k,v in datum.items() if datum['subject'] == subject}
#         new_data.append(filtered_dict)

#     #break out data by periods
#     comp_arrays = {}
#     for dict in new_data:
#         score_array=[]
#         component = dict['component_name']

#     #get student scores for each component
#     #use get percentile func. 