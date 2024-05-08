#Creating data for DB
import numpy as np
import pandas as pd
import sqlalchemy as sa
from models import*
from faker import Faker
from flask_login import current_user
from psycopg2.extensions import register_adapter, AsIs
register_adapter(np.int32, AsIs) #helps translate numpy data types for sqlalchemy
register_adapter(np.int64, AsIs)

#Using the terminal to add primlinary fake data
fake = Faker()

#THINGS TO REMEMBER
# When using pd.read_csv in terminal, use \\ on file path
# df.to_dict('index') or 'record'

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


def class_creation():
    x = 0
    query = sa.select(Staff)
    staff = db.session.scalars(query)
    while x <= 5:
        for s in staff:
            staff_class = make_fake_class(2021, 'Simple Pimple Academy', x, s.id)
            
            classroom = Classroom(**staff_class)
            db.session.add(classroom)
            db.session.commit

            roster = make_people(np.random.randint(8,15),0)
            for r in roster:
                student = Student(**r)
                sc = {'student_id': student.id,
                    'classroom_id': classroom.id}
                student_class = StudentClassroomAssociation(**sc)
                db.session.add(student)
                db.session.add(student_class)
                db.session.commit()

            x += 1


