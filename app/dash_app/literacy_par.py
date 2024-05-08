# import sqlalchemy as sa
# from dash import Dash, dash_table, dcc, html, Input, Output, callback
# from flask import Flask
# from flask_login import login_required, current_user
# import dash_bootstrap_components as dbc
# from dash.dependencies import Output, Input, State
# import plotly.express as px
# import pandas as pd
# from models import *
# from data_entry import routes, data_entry
# from call_backs import get_callbacks



# data = data_entry('Predictive Assessment of Reading', 'lfrancese')

# # Define the layout of the Dash app
# def lit_layout(dash_app):
#     dash_app.layout = html.Div([
#         html.Button('Submit', id="submit"),
#     get_callbacks(dash_app),
#     html.Div(id='test-par-data-entry'),
#         dash_table.DataTable(
#             id='table-editing',
#             columns=[{'id': i, 'name': i} for i in ['Student', 'Rapid Naming', 'Total Standardized Score', 'Letter Word Calling', 'Phonemic Awareness', 'Picture Naming']],
#             data=data,
#             editable=True
#         ),
#         dcc.Graph(id='test-par-data-entry-output')
#     ])

