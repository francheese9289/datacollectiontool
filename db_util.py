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

classroom_schoolyears_df = pd.DataFrame(ClassroomSchoolYear)
# room_types_reviewed = air_bnb.groupby(['room_type'], as_index = False).sum(numeric_only = True)[['room_type','number_of_reviews']]
# room_types_reviewed = room_types_reviewed.sort_values('number_of_reviews', ascending = False)
def user_rosters_v2(current_user):
    user = current_user
    user_classes = pd.DataFrame(ClassroomSchoolYear.query.filter_by('teacher_id == @staff_id'))
    user_students = pd.DataFrame(StudentClasses.query.filter_by('class_sy_id == user_classes.id')) 
    demo_ratings = customer_demographics.merge(surveys, on = 'customer_id', how = 'inner')
    demo_ratings.head()
#popular_hosts = host_data[(host_data.number_of_reviews >= 100) & (host_data.availability_365 == 0)]