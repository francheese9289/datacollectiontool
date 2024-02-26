from flask import Blueprint, render_template, flash, redirect, url_for, request, flash, session
from flask_login import login_required, current_user
from models import db, User, Student, AssessmentScores, login_manager
import pandas as pd
#from db_util import user_class_data

main = Blueprint('main', __name__, template_folder='main_templates')


@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    # user=current_user
    # roster_df = pd.DataFrame()

    # #filter for current_user's class data
    # if user.role_id > 0:
    #     roster_df = user_class_data(user.staff_id, user.role_id)

    # Render the profile page with the filtered roster
    return render_template('profile.html', roster_df=roster_df, user=user)

# @app.route('/')
# def home():
#     """Landing page."""
#     return render_template(
#         'index.jinja2',
#         title='Plotly Dash Flask Tutorial',
#         description='Embed Plotly Dash into your Flask applications.',
#         template='home-template',
#         body="This is a homepage served with Flask."
#     )