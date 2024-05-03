import sqlalchemy as sa
from dash import Dash, dash_table, dcc, html, Input, Output, callback
from flask import Flask
from flask_login import login_required, current_user
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd
from models import *
from helpers import * 




def par_entry_test(dash_app):
    par = data_entry('Predictive Assessment of Reading','lfrancese')

    dash_app.layout = html.Div([
        dash_table.DataTable(
            id='test-par-data-entry',
            columns =[{'id': i, 'name':i}for i in ['Student','Rapid Naming','Total Standardized Score','Letter Word Calling','Phonemic Awareness','Picture Naming']],
            data=par,
            editable=True
        ),
        dcc.Graph(id='test-par-data-entry-output')    
    ])

