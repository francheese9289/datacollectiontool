from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import current_user
from models import db, User, Staff, Student, AssessmentStandard, AssessmentComponent, AssessmentScore, StudentClassroomAssociation, Classroom
from forms import AssessmentScoreForm, ComponentForm
import sqlalchemy as sa

api = Blueprint('api',__name__, url_prefix='/api', template_folder='data_templates')

@api.route('/data_entry', methods=['GET', 'POST'])
def data_entry(): # <this will need to accept an assessment name as a parameter>
    #find current user and their most recent classroom
    user=current_user
    staff = db.session.scalar(sa.select(
        Staff).where(Staff.id == user.staff_id))
    current_class = staff.staff_classrooms[-1] #returns classroom object
    assessment = 'Predictive Assessment of Reading' #will be a variable

    #gather information for all students in that classroom
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
            AssessmentComponent.assessment_name == assessment).order_by(
                AssessmentComponent.component_name)).all()
    #parent form
    form = AssessmentScoreForm()
    #child form
    component_form = ComponentForm()
    
    for component in components:
        component_form.component_id = component.id
        form.components.append_entry(component_form) 
        #.append_entry does not allow for form data in the same (child) form, hence the workaround below

    if form.validate_on_submit():
        period = request.form.get('period')
        
        for student_data in roster_data:
            student_id = student_data['id']
            
            for component in components:
                component_id = component.id
                
                # using html form functionality to get the student's score for each component
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
        return redirect(url_for('main.user', username=user.username))

    return render_template('data_entry.html', form=form, components=components, component_form=component_form, roster_data=roster_data)

