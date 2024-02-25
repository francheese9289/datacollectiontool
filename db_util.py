from models import *
import pandas as pd


def user_class_data(staff_id, role_id):
    """Pandas dataframe to pull classroom data into staff profiles"""
    """MIGHT CHANGE THIS TO DICT INSTEAD OF DF?"""
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
    user_rosters = pd.DataFrame()

    #role_id for teachers
    if role_id == 2:
        user_rosters = roster_df.query('teacher_id == @staff_id')
    #add role_id for principals (might be a different function)& admin
    return user_rosters