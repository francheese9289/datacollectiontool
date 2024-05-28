import math
import sqlalchemy as sa
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from models import db, AssessmentComponent, AssessmentScore
from forms import AssessmentScoreForm, ComponentForm, EditAssessmentScoreForm
from app.services.charts import *
from app.services.data_analysis import *
from app.services.api_views import *
import numpy as np

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
    user=current_user
    current_class = user.get_current_classroom()
    classroom_info = current_class.to_dict()
    data = get_data('21-SPA-0')

    math_data = data[(data.subject == 'math')]
    lit_data = data[(data.subject == 'literacy')]
    math_fun_fig= make_funnel(math_data)
    math_bar_fig = make_bar_fig(math_data)
    lit_fun_fig= make_funnel(lit_data)
    lit_bar_fig = make_bar_fig(lit_data)

    figs = [lit_bar_fig, math_bar_fig, lit_fun_fig, math_fun_fig]

    return render_template(template_name_or_list='class_dashboard.html', classroom_info=classroom_info, classroom_id=current_class, figs=figs)