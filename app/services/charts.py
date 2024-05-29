from enum import unique
from hashlib import file_digest
import json
# from pkgutil import get_subject_data
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.subplots as make_subplots
import pandas as pd
import numpy as np
import plotly.express as px
from models import *
from app.services.data_analysis import add_ranks



#each df row = funnel level
def make_funnel(data):
    """
    Funnel charts for avg scores and class & national rankings in a single subject.
    **later iterations will need to separate assessment types, currently only have 1 assess/subject**
    """

    #average student scores and standards for all components in a single period
    subject_data = data.groupby(['period','student']).mean(numeric_only = True)[['period','student','student_score','tier_1','tier_2','tier_3']]

    ranked_data = (period.apply(add_ranks) for period in subject_data['periods'])

    #subject_data for labelling
    periods = {1:'fall', 2:'winter', 3:'spring'}
    ranked_data['p_name'] = ranked_data['period'].map(periods)
    subject = subject_data.iloc[1,6] #gets name of subject (i.e. literacy, math, sel)

    df = ranked_data.groupby(['period','rank']).nunique()[['period','rank','student']]


    fig = px.bar(df, x='student', y='rank', color='tier', facet_row='p_name', 
                    width=800, height=400,
                    labels= {'p_name':'Period','student':'Student Cnt','class_rank':'Rank'},
                    title=f'Student class_rank Rankings in {subject.title()}')


    fig = fig.to_html(full_html=False)

    return fig


def make_bar_fig(subject_data):
    '''Create a highlevel view of assessment subject_data by subject'''

    
    df = subject_data.groupby(['period','component_name','student_score'], as_index=False).agg(
        student_score = ('student_score', np.mean)
    )

    #subject_data for labelling
    subject = subject_data.iloc[1,6]
    periods = {1:'fall',2:'winter',3:'spring'}
    df['p_name'] = df['period'].map(periods)
    
    
    fig = px.bar(df, x='component_name', y='student_score', facet_row='p_name', color='component_name',
                labels={'component_name':'Components','student_score':'Avg Score','p_name':'p'},
                width=800, height=800,
                title=f'Class Averages in {subject.title()} by Period')

    fig_html = fig.to_html(full_html=False)
    return fig_html



# def make_fig(df): #boxplot
    
#     fig = px.boxplot_frame(df, x=df['component_name'], y=df['student_score'])
    

#     # overall layout
#     fig_layout = {
#         "title":df['assessment_name'][0],
#         "font_family":"Open Sans",
#         "colorway":px.colors.qualitative.Dark2
#     }

#     fig.update_layout(fig_layout)
#     #x axis
#     labels= {
#         'component_name': 'Components',
#         'student_score': 'Student Scores'
#     }
#     x_layout = {
#         "categoryorder":"category ascending"
#         }
    
#     fig.update_xaxes(x_layout)
#     fig_html = fig.to_html(full_html=False)
#     return fig_html


# def make_table(df, assessment_name):
#     df = df[(df.assessment_name == assessment_name)]
#     df = df.set_index(['student','period','component_name'])
#     grouped = df.groupby(level=0)
#     asjson = json.dumps(df)

#     fig = go.Figure(subject_data=[go.Table(
#         header=dict(values=['Student','Period','Component','Score','class_rank'],
#                     fill_color='paleturquoise',
#                     align='left'),
#         cells=dict(values=[asjson.student, asjson.period, asjson.component_name, asjson.student_score, asjson.class_rank],
#                 fill_color='lavender',
#                 align='left'))
#                 ])

#     fig_html = fig.to_html(full_html=False)

#     return fig_html
    