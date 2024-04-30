import sqlalchemy as sa
from flask import render_template, Blueprint
from wtforms.validators import ValidationError
from models import User, Staff, Student, AssessmentScore, AssessmentStandard, StudentClassroomAssociation, db
from forms import PARScoreForm, PARTable
from flask_login import current_user

data = Blueprint('data', __name__, template_folder='data_templates')

@data.route('/data_entry', methods=['GET', 'POST'])
def data_entry():
    form = PARTable()
    # if request.method == 'POST' & form.validate_on_submit():
    user = current_user
    staff = db.session.scalar(sa.select(Staff).where(Staff.id == user.staff_id))
    current = staff.staff_classrooms[-1] #return classroom object
    students = current.class_students
    
    if form.validate_on_submit():
        for field in form.fields:
            score = AssessmentScore(
                student_score = form.,
                assessment_id = ,

            )
    return render_template('literacy.html', students=students, form=form)

# def edit_data(assessment_id): #pull in correct sub form?
#     assessment = 
#     form = form
#     if request.method == 'POST' and form.validate():
#         form.populate_obj()