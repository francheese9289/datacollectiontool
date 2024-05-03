from dash import Dash, dash_table, dcc, html, Input, Output, callback
from flask import Flask
from flask_login import login_required, current_user
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd
from models import *
from helpers import data_entry


def init_dashboard(server):
    dash_app = Dash(
        server=server,
        routes_pathname_prefix='/dash/',
        external_stylesheets=[dbc.themes.LITERA]
        )
    
    par_entry_test(dash_app)

    return dash_app.server

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

    for k in par:
        print (k)

   # basic_layout(dash_app)
    # basic_table(dash_app)
    # display_output(dash_app)
    # @dash_app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
    # def display_page(pathname):
    #     if pathname == '/dash/literacy':
    #         return lit_dash.layout()
    #     elif pathname == '/dash/page2':
    #         return page2.layout()
    #     else:
    #         return '404 Page Not Found'
    # # Define layout for the Dash app
    # dash_app.layout = html.Div([
    #     dcc.Location(id='url', refresh=False),
    #     html.Div(id='page-content')
    # ])

#REUSEABLE FUNCTION for creating a datatable
# def generate_table(dataframe, max_rows=10):
#     return html.Table([
#         html.Thead(
#             html.Tr([html.Th(col) for col in dataframe.columns])
#         ),
#         html.Tbody([
#             html.Tr([
#                 html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#             ]) for i in range(min(len(dataframe), max_rows))
#         ])
#     ])

