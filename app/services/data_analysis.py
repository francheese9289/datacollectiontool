import json
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.subplots as make_subplots
import pandas as pd
import plotly as px
from models import *
from app.services.charts import *


        
def get_assessment_name(component_id):
    component = AssessmentComponent.get_by_id(component_id)
    if component:
        return component.name
    return None

def get_data(classroom): #could probably simplify this now that I have ids for class assessments
    
    class_scores = db.session.execute(
        sa.select(AssessmentScore).where(AssessmentScore.classroom_id == classroom)
    ).scalars().all()

    # create dicts of component & student ids
    component_ids = {score.component_id for score in class_scores}
    student_ids = {score.student_id for score in class_scores}
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
            AssessmentStandard.component_id.in_(component_ids),
            AssessmentStandard.grade_level.in_([c.grade_level for c in classrooms]),
            AssessmentStandard.period.in_([score.period for score in class_scores])
        )
    ).scalars().all()

    # Create dictionaries to map data OBJECTS by IDs
    component_map = {comp.id: comp for comp in components}
    student_map = {student.id: student for student in students}
    classroom_map = {cls.id: cls for cls in classrooms}
    standard_map = {(std.component_id, std.grade_level, std.period): std for std in standards}

    data = []
    for score in class_scores:
        comp = component_map[score.component_id]
        student = student_map[score.student_id]
        classroom = classroom_map[score.classroom_id]
        standard_key = (score.component_id, classroom.grade_level, score.period)
        standard = standard_map.get(standard_key)

        if standard:
            if score.student_score <= standard.tier_1:
                tier = 'tier 1'
            elif score.student_score <= standard.tier_2:
                tier = 'tier 2'
            else:
                tier = 'tier 3'
        else:
            tier = None

        data.append({
            'score_id': score.id,
            'student_score': score.student_score,
            'component_id': score.component_id,
            'component_name': comp.component_name,
            'assessment_name': comp.assessment_name,
            'subject': comp.subject,
            'period': score.period,
            'student': student.full_name,
            'classroom_id': score.classroom_id,
            'grade_level': classroom.grade_level,
            'tier': tier
        })
    df = pd.DataFrame(data)
    
    return df



