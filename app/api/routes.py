import sqlalchemy as sa
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from models import db, AssessmentComponent, AssessmentScore
from forms import AssessmentScoreForm, ComponentForm, EditAssessmentScoreForm
from app.services.data_analysis import *
from app.services.api_views import *
import numpy as np
from psycopg2.extensions import register_adapter, AsIs
register_adapter(np.int32, AsIs)
register_adapter(np.int64, AsIs)

api = Blueprint('api', __name__, url_prefix='/api', template_folder='../templates/api')
templates = Blueprint('templates', __name__)

@api.route('/', methods=['GET', 'POST'])
def data_entry_params():
    """landing page for data entry"""
    if request.method == 'GET':
        return render_data_entry_parameters()
    elif request.method == 'POST':
        return process_data_entry_parameters()
    
@api.route('/data_entry/<string:assessment_name>', methods=['GET', 'POST'])
def data_entry(assessment_name):
    """API endpoint for data entry"""
    period = request.args.get('period')
    if request.method == 'GET':
        return render_data_entry_template(assessment_name, period)
    elif request.method == 'POST':
        return process_data_entry_request(assessment_name, period)


@api.route('/data_entry/edit', methods=['GET', 'POST'])
def edit_data_params():
    """Landing page for editing data"""
    if request.method == 'GET':
        return render_edit_data_parameters()
    elif request.method == 'POST':
        return process_edit_data_parameters()

def render_edit_data_parameters():
    """Parameters for editing score data in database"""
    user = current_user
    current_class = user.get_current_classroom()  # returns classroom object
    class_score_data = get_data(current_class.id)

    assessments = class_score_data['assessment_name'].unique()  # assessments already taken
    periods = {1: 'fall', 2: 'winter', 3: 'spring'}
    available_periods = {assessment:[periods] for assessment in class_score_data['assessment_name'] for period in class_score_data['period']}
    # Create a dictionary to hold available periods for each assessment

    return render_template('edit_data_params.html', assessments=assessments, periods=periods, available_periods=available_periods)

def process_edit_data_parameters():
    print(request.form)
    assessment = request.form.get('assessment')
    period = request.form.get('period')
    if assessment and period:
        return redirect(url_for('api.edit_data', assessment_name=assessment, period=period))
    else:
        flash('Please select both an assessment and a period', 'error')
        return redirect(url_for('api.edit_data_params'))

@api.route('/data_entry/edit/<string:assessment_name>', methods=['GET', 'POST'])
def edit_data(assessment_name):
    """API endpoint for editing data"""
    period = request.args.get('period')
    if request.method == 'GET':
        return render_edit_data_template(assessment_name, int(period))
    elif request.method == 'POST':
        return process_edit_data_request(assessment_name, int(period))



@api.route('/classroom/<string:classroom_id>', methods=['GET', 'POST'])
@login_required
def class_dashboard(classroom_id, method='GET'):
    '''
    This function renders the dashboard page for the user.
    It is expected to display data related to the user's classroom, including literacy, math, and SEL metrics.
    For admin dashboards, it will include grade level and school level data in the future.
    '''
    #find current user and their most recent classroom
    user=current_user
    current_class = db.session.scalar(sa.select(Classroom).where(
        Classroom.id == classroom_id
    ))
    print(current_class) #this is printing the correct classroom
    classroom_info = current_class.to_dict()
    df = get_data('21-SPA-0')
    fig = make_fig(df)
    
    return render_template('class_dashboard.html', classroom_info=classroom_info, classroom_id=current_class, fig=fig)


 # user=current_user
    # current_class = user.get_current_classroom() #returns classroom object
    # class_score_data = get_data(current_class.id)
    

    # components = class_score_data[['component_id', 'component_name']].drop_duplicates().sort_values('component_name').to_dict('records')

    # selected_period = request.form.get('period') or class_score_data['period'].unique()[0]
    # filtered_score_data = class_score_data[class_score_data['period'] == int(selected_period)]

    
    # data = {} #dict for pertinent student score data needed to populate form
    # for _, row in filtered_score_data.iterrows(): #underscore used to ignore index in loop!
    #     student = row['student'] #student_name
    #     if student not in data:
    #         data[student] = {'scores': []} #list of scores for given assessment
    #     data[student]['scores'].append({
    #         'component_id': row['component_id'],
    #         'score_id': row['score_id'],
    #         'score_value': row['student_score']
    #     })

    # form = EditAssessmentScoreForm()
    
    # if form.validate_on_submit():
    #     period = request.form.get('period')
        
    #     for student, student_data in data.items():
    #         for score_data in student_data['scores']:
    #             score_id = score_data['score_id']
    #             student_score = request.form.get(f'student_score_{score_id}')

    #             if score_id and student_score is not None:
    #                 update_score = db.session.query(AssessmentScore).get(score_id)
    #                 if update_score:
    #                     update_score.period = period
    #                     update_score.student_score = student_score
    #                     db.session.commit()

    # return render_template('edit_data.html', form=form, data=data, components=components, periods=class_score_data['period'].unique(), selected_period=selected_period)
            




# @api.route('/data_entry/<string:subject>/<string:assessment_name>', methods=['GET', 'POST']) #I would like to clean this function up
# def data_entry_lit(): 
#     '''Populate table for user data entry.'''
#     assessment_name = 'Predictive Assessment of Reading' 
#     user=current_user

#     current_class = user.get_current_classroom() 
#     roster_data = current_class.classroom_roster()
#     print(roster_data)

#     components = db.session.scalars(
#         sa.select(AssessmentComponent).where(
#             AssessmentComponent.assessment_name == assessment_name).order_by(
#                 AssessmentComponent.component_name)).all()
    
#     #main form
#     form = AssessmentScoreForm()
#     #nested form
#     component_form = ComponentForm() 

#     if form.validate_on_submit():
#         period = request.form.get('period')
        
#         for student_data in roster_data:
#             student_id = student_data['student_id']
            
#             for component in components:
#                 component_id = component.id
                
#                 # using html form to get the student's score
#                 score_key = f"score_{student_id}_{component_id}"
#                 student_score = request.form.get(score_key)
                
#                 # create a new score instance and populate its attributes
#                 new_score = AssessmentScore()
#                 new_score.period = period
#                 new_score.component_id = component_id
#                 new_score.student_id = student_id
#                 new_score.classroom_id = current_class.id
#                 new_score.student_score = student_score
#                 new_score.class_assessment_id = new_score.class_assessment_id()
#                 # add the score instance to the session
#                 db.session.add(new_score)
#         db.session.commit()

#         flash('Data entered successfully!', 'success')
#         # Need to change this redirect to the dash or a data entry landing page
#         return redirect(url_for('api.data_entry_lit'))
#     return render_template('literacy.html', form=form, components=components, component_form=component_form, roster_data=roster_data)

# @api.route('/data_entry/math', methods=['GET', 'POST'])
# def data_entry_math(): 
#     assessment_name = 'Primary Number & Operations Assessment' 
#     user=current_user

#     current_class = user.get_current_classroom() 
#     roster_data = current_class.classroom_roster()

    
#     #get all components for a given assessment 
#     components = db.session.scalars(
#         sa.select(AssessmentComponent).where(
#             AssessmentComponent.assessment_name == assessment_name).order_by(
#                 AssessmentComponent.component_name)).all()
#     #main form
#     form = AssessmentScoreForm()
#     #nested form
#     component_form = ComponentForm()
#     if form.validate_on_submit():
#         period = request.form.get('period')
        
#         for student_data in roster_data:
#             student_id = student_data['id']
            
#             for component in components:
#                 component_id = component.id
                
#                 # using html form to get the student's score
#                 score_key = f"score_{student_id}_{component_id}"
#                 #I THINK using 'request' allows for CSRF protection?
#                 student_score = request.form.get(score_key)
                
#                 # create a new score instance and populate its attributes
#                 new_score = AssessmentScore()
#                 new_score.period = period
#                 new_score.component_id = component_id
#                 new_score.student_id = student_id
#                 new_score.classroom_id = current_class.id
#                 new_score.student_score = student_score
                
#                 # add the score instance to the session
#                 db.session.add(new_score)
#         db.session.commit()

#         flash('Data entered successfully!', 'success')
#         return redirect(url_for('api.index'))

#     return render_template('math.html', assessment_name=assessment_name, form=form, components=components, component_form=component_form, roster_data=roster_data)
