from flask import Blueprint, render_template, flash, redirect, url_for, request, flash, session
from flask_login import login_required
from models import db, User, Student, AssessmentScores, login_manager
import pandas as pd
import plotly.express as px
from db_util import user_class_data

main = Blueprint('main', __name__, template_folder='main_templates')


@main.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)


# @main.route('/dashboard', methods=['GET'])
# def dashboard():
#     user_id = session['user_id']
#     if user_id in session:
#         scores = AssessmentScores.query.all()
#         data = pd.DataFrame([(score.id, score.student_score, score.assessment_id) for score in scores],
#                         columns = ['id', 'student_score','assessment_id'])
#     table_html = data.to_html()
#     return render_template('dashboard.html', table_html=table_html)

# #put this back in when not testing or logged in 
#     # if 'user_id' not in session:
#     #     flash('Please log in first.', 'danger')
# #     #     return redirect(url_for('login'))

#     
#     user = User.get(user_id)
#     # return render_template('dashboard.html', user=user)

@main.route('/profile/<user_id>')
@login_required
def profile(user_id):
    user_id = session['user_id']
    user = User.query.get(user_id)
    is_staff = user.is_staff_member()
    role_id = user.get_role_id()
    staff_id = None
    if is_staff:
        staff_id = user.staff_id  

    if staff_id > 0:
        roster_df = user_class_data(staff_id, is_staff, role_id)

    # Render the profile page with the filtered roster
    return render_template('profile.html', roster_df=roster_df)
        
    # return render_template('profile.html', user=user)


# @main.route('/testing')
# def test():
#     user_id = session['user_id']
#     user =