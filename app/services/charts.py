import json
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.subplots as make_subplots
import pandas as pd
import plotly as px
from models import *

def make_fig(df): #boxplot
    
    fig = px.boxplot_frame(df, x=df['component_name'], y=df['student_score'])
    

    # overall layout
    fig_layout = {
        "title":df['assessment_name'][0],
        "font_family":"Open Sans",
        "colorway":px.colors.qualitative.Dark2
    }

    fig.update_layout(fig_layout)
    #x axis
    labels= {
        'component_name': 'Components',
        'student_score': 'Student Scores'
    }
    x_layout = {
        "categoryorder":"category ascending"
        }
    
    fig.update_xaxes(x_layout)
    fig_html = fig.to_html(full_html=False)
    return fig_html


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
    