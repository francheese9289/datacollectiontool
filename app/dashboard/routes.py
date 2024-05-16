import sqlalchemy as sa
from flask import Blueprint, request, render_template, redirect, url_for, flash
from models import User, Staff, Student, Classroom, StudentClassroomAssociation, AssessmentStandard, AssessmentScore, db
from flask_login import current_user, login_required
from queries import *
import altair as alt


dashboard = Blueprint('dashboard', __name__, url_prefix='/insights', template_folder='dash_templates')
#need to make an index page for the dashboard
#idk how tied I am to the 'insights' naming convention, using dashboard for now
@dashboard.route('/classroom/<string:classroom_id>', methods=['GET', 'POST'])
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
    print(df)
    
    return render_template('class_dashboard.html', classroom_info=classroom_info, classroom_id=current_class, fig=fig)




