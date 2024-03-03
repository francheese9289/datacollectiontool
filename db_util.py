from models import *
import pandas as pd
from flask_login import current_user
from sqlalchemy import text

def fetch_all_rosters(staff_id):
    # Use SQLAlchemy to execute a raw SQL query on the view
    query = text(f'SELECT * FROM v_detailed_rosters WHERE teacher_id={staff_id}')
    rosters = db.session.execute(query).fetchall()
    return rosters

def group_rosters_by_class(rosters):
    rosters_by_class = {}

    for roster in rosters:
        class_id = roster[3]

        if class_id not in rosters_by_class:
            rosters_by_class[class_id] = []

        rosters_by_class[class_id].append(roster)

    return rosters_by_class

# def fetch_lit_scores(**kwargs):

#     for key, value in kwargs:
#         query = text(f'SELECT * FROM v_detailed_lit_scores WHERE {key}={value}')
#         result = db.session.execute(query).fetchall()

def fetch_lit_scores():
     query = text(f'SELECT * FROM v_detailed_lit_scores')
     result = db.session.execute(query).fetchall()
     return result

# def group_lit_scores(school_id):
#     query = text(f'select 
# year_id,
# avg(student_score) as avg_score,
# assessment_id,
# student_id, 
# school_id,
# short_name,
# grade_level_id,
# classroom_id,
# teacher_id 
# from v_detailed_lit scores 
# group by year_id, assessment_id, student_id, school_id,
# short_name,
# grade_level_id,
# classroom_id,
# teacher_id ')

#     create view v_detailed_lit_scores as
# select 
# vals.student_score,
# vals.assessment_id,
# vals.student_id,
# vals.csp_id,
# vals.periodid,
# vals.cs_id,
# vals.subject,
# vdr.grade_level_id,
# vdr.year_id,
# vdr.teacher_id,
# vdr.student_full_name,
# vdr.staff_full_name
# from v_all_lit_scores vals
# join v_detailed_rosters vdr on
# vals.student_id=vdr.student_id and vals.cs_id=vdr.class_sy_id;