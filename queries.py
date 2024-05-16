from flask import request, flash, redirect, url_for, render_template
from flask_login import current_user
from models import *
from plotly import utils
import plotly.graph_objs as go
import pandas as pd
import plotly as px


# This method is much faster than creating a df as a class attribute
# Use this to edit assessment form data as well?
def get_data(classroom):
    
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


def make_fig(df):
    fig = px.boxplot_frame(df, x=df['component_name'], y=df['student_score'])
    fig_html = fig.to_html(full_html=False)

    # overall layout
    fig_layout = {
        "title":df['assessment_name'][0],
        "font_family":"Open Sans",
        "colorway":px.colors.qualitative.Dark2
    }

    fig.update_layout(fig_layout)
    #x axis
    # labels= {'Letter Word Calling': 'PARLWC', ''}
    x_layout = {
        "categoryorder":"category ascending"
        }
    
    fig.update_xaxes(x_layout)
    return fig_html


















# alt.themes.register("my_custom_theme", urban_theme)
# alt.themes.enable("my_custom_theme")



# def high_level_classroom_plots(data): #just classroom for now
#     '''high level view of all student scores in a particular subjects.
#     Data is a dataframe containing score,period,student, classroom, compomnent, assessment, comp name, subject'''

#     # math_base = alt.Chart(data, title='Literacy & Math Scores').mark_bar().encode(
#     # alt.X('component_name:N').title('Assessment Component'),
#     # alt.Y('student_score:Q').title('Student Scores').scale(zero=False),
#     # color='tier:N').transform_filter(alt.datum.subject =='math')

#     lit_base = alt.Chart(data, title='Literacy Scores').mark_bar().encode(
#     alt.X('component_name:N').title('Assessment Component'),
#     alt.Y('student_score:Q').title('Student Scores').scale(zero=False),
#     color=alt.Color('tier:N'))
    
#     # chart = alt.hconcat(lit_base, math_base, spacing=10)
#     lit_base.save('app/dashboard/dash_templates/temp_lit_scores.html') 


# # def make_plot(data):

#     # plot = alt.Chart(data, title=f'{data.subject.title()} Scores').mark_boxplot(extent="min-max").encode(
#     #         x=alt.X('component_name').title('Assessment Component'),
#     #         y=alt.Y('student_score').title('Student Scores').scale(zero=False),
#     #         color=alt.Color('component_name').title('Component'))


# # def math_assessment_plots(data):


