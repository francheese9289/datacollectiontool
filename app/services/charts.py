import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.subplots as make_subplots
import pandas as pd
import numpy as np
import plotly.express as px
from models import *


#each df row = funnel level
def make_funnel(data):
    """Funnel chart logic"""
    #create pct rank column
    data['percentile_rank'] = data.groupby(['period'])['student_score'].rank(pct=True)

    data['tier'] = data['percentile_rank'].apply(assign_tier)

    #data for labelling
    periods = {1:'fall',2:'winter',3:'spring'}
    subject = data.iloc[1,6]
    
    funnel_df = data.groupby(['period','tier'], as_index=False).nunique()[['period','tier','student']]

    funnel_df['p_name'] = funnel_df['period'].map(periods)

    funnel_df = funnel_df.sort_values('tier', ascending=False)

    fig = px.funnel(funnel_df, x='student', y='tier', color='tier', facet_col='p_name',
                    width=800, height=400,
                    labels= {'p_name':'Period','student':'Student Cnt','tier':'Tier'},
                    title=f'Student Tier Rankings in {subject.title()}')


    fig = fig.to_html(full_html=False)

    return fig

def get_unique_cnt(array):
    unique_count = np.unique(array, return_counts=True)
    return unique_count

def assign_tier(percentile_rank):
    if percentile_rank <= 0.1:
        return 'Tier 3'
    elif percentile_rank <= 0.5:
        return 'Tier 2'
    else:
        return 'Tier 1'


def make_bar_fig(data):
    '''Create a highlevel view of assessment data by subject'''

    
    df = data.groupby(['period','component_name','student_score'], as_index=False).agg(
        avg_score = ('student_score', np.mean)
    )

    #data for labelling
    subject = data.iloc[1,6]
    periods = {1:'fall',2:'winter',3:'spring'}
    df['p_name'] = df['period'].map(periods)
    
    
    fig = px.bar(df, x='component_name', y='avg_score', facet_row='p_name', color='component_name',
                labels={'component_name':'Components','avg_score':'Avg Score','p_name':'p'},
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

#     fig = go.Figure(data=[go.Table(
#         header=dict(values=['Student','Period','Component','Score','Tier'],
#                     fill_color='paleturquoise',
#                     align='left'),
#         cells=dict(values=[asjson.student, asjson.period, asjson.component_name, asjson.student_score, asjson.tier],
#                 fill_color='lavender',
#                 align='left'))
#                 ])

#     fig_html = fig.to_html(full_html=False)

#     return fig_html
    