#Creating data for DB
import numpy as np
import sqlalchemy as sa
from models import *
from faker import Faker
from psycopg2.extensions import register_adapter, AsIs

register_adapter(np.int32, AsIs) #helps translate numpy data types for sqlalchemy
register_adapter(np.int64, AsIs)

fake = Faker()

#THINGS TO REMEMBER
# When using pd.read_csv in terminal, use \\ on file path
# df.to_dict('index') or 'record'


def class_creation(year, school):
    x = 0
    query = sa.select(Staff)
    staff = db.session.scalars(query)
    while x <= 5:
        for s in staff:
            staff_class = make_fake_class(year, school, x, s.id)
            
            classroom = Classroom(**staff_class)
            print(f'new class: {classroom}')
            db.session.add(classroom)
            db.session.commit
#TEST THIS PORTION OUT----------------------------
            if classroom.grade_level >= 1:
                roster = db.session.scalars(sa.select(Classroom.class_students).where(sa.and_(
                    Classroom.grade_level == classroom.grade_level-1),(Classroom.school == classroom),(Classroom.school_year==classroom.school_year-1)))
                sc = [{'student_id': r.id, 'classroom_id':classroom.id} for r in roster]
                student_class = StudentClassroomAssociation(**sc)
                print (f'student class moving up: {student_class}')
                db.session.add(student_class)
                db.session.commit()
###-----------------------------------------------
            else:
                roster = make_people(np.random.randint(8,15),0)
                for r in roster:
                    student = Student(**r)
                    sc = {'student_id': student.id,
                        'classroom_id': classroom.id}
                    student_class = StudentClassroomAssociation(**sc)
                    print (f'new students: {student_class}')
                    db.session.add(student)
                    db.session.add(student_class)
                    db.session.commit()
            x += 1

def make_fake_class(year, school, grade_level, teacher_id):
    '''Provide data needed to make a classroom'''
    #is this an appropriate place for **kwargs? too specific?
    year_id = year-2000
    school_id = (f"{school.split(' ')[0][0]}{school.split(' ')[1][0]}{school.split(' ')[2][0]}") #taking initials-could probably just use regex
    my_class = {
        'id':(f'{year_id}-{school_id}-{grade_level}'),
        'school_year': year,
        'school_name': school,
        'grade_level': grade_level,
        'teacher_id': teacher_id,
    }

    return my_class

def make_emails(person_name):
    '''Create email using first initial & last name of person's full name'''
    p= person_name.split(" ")
    first_initial = p[0][0]
    last_name = p[1]
    email = (f'{first_initial}{last_name}@simpleschooldistrict.org').lower()
    return email

def make_people(num,role):
    '''Generate fake student or staff data'''
    fake_names = [] #list of fake student names
    for i in range(num):
        full_name = f'{fake.first_name()} {fake.last_name()}'
        fake_names.append(full_name)
    if role == 0:
        fake_people = [{'id': np.random.choice(np.arange(10000,20000),replace=False),
            'full_name':(fake_names[x]),
            'email': make_emails(fake_names[x])
            }for x in range(num)]
    else:
        fake_people = [{'id': np.random.choice(np.arange(1100,2000),replace=False),
            'full_name':(fake_names[x]),
            'email': make_emails(fake_names[x]),
            'role_id': role}for x in range(num)]
    return fake_people

# ADD SCORE DATA

def add_fake_scores(class_id, assessment_name, period):
    class_object = db.session.scalar(sa.select(Classroom).where(Classroom.id == class_id))
    roster = class_object.classroom_roster()
    components = db.session.scalars(sa.select(AssessmentComponent).where(AssessmentComponent.assessment_name==assessment_name)).all()
    
    for student in roster:
        for component in components:
            high = db.session.scalar(sa.select(AssessmentStandard.tier_3).where(AssessmentStandard.component_id == component.id))
            score = np.random.randint(0, high)
            new_score = AssessmentScore()
            new_score.period = period
            new_score.component_id = component.id
            new_score.student_id = student['student_id']
            new_score.classroom_id = class_id
            new_score.student_score = score
            new_score.class_assessment_id = new_score.class_assessment_id()
            db.session.add(new_score)
    db.session.commit()
    