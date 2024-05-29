import json
from numpy import percentile
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.subplots as make_subplots
import pandas as pd
import plotly as px
from models import *
from app.services.charts import *
from scipy.stats import percentileofscore


def get_data(classroom): 
    '''faster data extraction method'''
    class_scores = db.session.execute(
        sa.select(AssessmentScore).where(AssessmentScore.classroom_id == classroom)
    ).scalars().all()

    # create dicts of component & student ids
    component_ids = {score.component_id for score in class_scores}
    student_ids = {score.student_id for score in class_scores}
    standard_ids = {score.standard_id for score in class_scores}
    classroom_ids = {classroom}

    # Fetch RELATED data (from above dicts) in bulk
    components = db.session.execute(
        sa.select(AssessmentComponent).where(AssessmentComponent.id.in_(component_ids))
    ).scalars().all()
    students = db.session.execute(
        sa.select(Student).where(Student.id.in_(student_ids))
    ).scalars().all()
    classrooms = db.session.execute(
        sa.select(Classroom).where(Classroom.id.in_(classroom_ids))
    ).scalars().all()
    standards = db.session.execute(
        sa.select(AssessmentStandard).where(
            AssessmentStandard.id.in_(standard_ids))
    ).scalars().all()

    # Create dictionaries to map data OBJECTS by IDs
    component_map = {comp.id: comp for comp in components}
    student_map = {student.id: student for student in students}
    classroom_map = {cls.id: cls for cls in classrooms}
    standard_map = {std.id: std for std in standards}

    data = []
    for score in class_scores:
        comp = component_map[score.component_id]
        student = student_map[score.student_id]
        classroom = classroom_map[score.classroom_id]
        standard = standard_map[score.standard_id]

        
        data.append({
            'score_id': score.id,
            'student_score': score.student_score,
            'component_id': score.component_id,
            'component_name': comp.component_name,
            'assessment_name': comp.assessment_name,
            'benchmark':comp.benchmark,
            'subject': comp.subject,
            'period': score.period,
            'student': student.full_name,
            'classroom_id': score.classroom_id,
            'grade_level': classroom.grade_level,
            'standard_id': standard.id,
            'tier_1': standard.tier_1,
            'tier_2': standard.tier_2,
            'tier_3':standard.tier_3
        })
    df = pd.DataFrame(data)
    
    return df

def add_ranks(period_data):
    '''returns tier level for score data whether singular or aggregated'''
    ranks = ['national','class']
    period_data = (([d.id, d.student, d.student_score, rank, d.tier_1, d.tier_2, d.tier_3] for d in period_data)for rank in ranks)

    for score in period_data:
        if period_data.rank == 'class':
            score['pct'] = period_data.groupby(['student'])[['student_score']].rank(pct=True)
            score['tier'] = (('Tier 3' if score.student_score <= .1 else 'Tier 2' if score.student_score <= .5 else 'Tier 3') for score in period_data)
        elif period_data.rank == 'national':
            ntl_stds = range(period_data.tier_1)
            score['pct'] = percentileofscore(ntl_stds, score['student_score'])
            score['tier'] = (('Tier 3' if score.student_score <= data.tier_3 else 'Tier 2' if score.student_score <= data.tier_2 else 'Tier 3') for data in period_data)
    return period_data
