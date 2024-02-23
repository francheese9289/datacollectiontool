from flask_sqlalchemy import SQLAlchemy
from flask import current_app, g, session, Blueprint
from models import *
import pandas as pd


def user_class_data(staff_id, is_staff, role_id):
    """Pandas dataframe to pull classroom data into staff profiles"""
    class_roster = db.session.query(
        Student.student_full_name,
        Staff.staff_full_name,
        ClassroomSchoolYear.id,
        ClassroomSchoolYear.teacher_id,
        ClassroomSchoolYear.school_id,
        ClassroomSchoolYear.year_id,
        Classroom.grade_level_id,
        StudentClasses
    ).join(
        ClassroomSchoolYear, StudentClasses.class_sy_id == ClassroomSchoolYear.id
    ).join(
        Student, StudentClasses.student_id == Student.id
    ).join(
        Staff, ClassroomSchoolYear.teacher_id == Staff.staff_id
    ).join(
        Classroom, ClassroomSchoolYear.classroom_id == Classroom.id
    ).all()

    roster_df = pd.DataFrame(class_roster)

    if is_staff and role_id == 2:
        user_rosters = roster_df.filter_by(roster_df.teacher_id==staff_id)
    return user_rosters