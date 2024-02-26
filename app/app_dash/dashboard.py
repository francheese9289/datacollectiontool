# app_dash/dashboard.py
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input 
from db_util import *


def init_dashboard(server):
    # Create Dash app instance
    dash_app = dash.Dash(server=server, routes_pathname_prefix='/dash/', external_stylesheets=[dbc.themes.LITERA])
    
    # Create dashboard layout
    dash_app.layout = html.Div([
        html.H1('Header',
                style={'color':'blue',
                       'fontSize':'40px',
                       'marginLeft': '20px'}),
        html.H2('Sub Heading'),
        dbc.Tabs([
            dbc.Tab([
                html.Ul([
                    html.Li('list item'),
                    html.Li('list item'),
                ]),
            ], label='Overview'),
            dbc.Tab([
                html.Ul([
                    html.Br(),
                    html.Li('list item'),
                    html.Li(['Website: ',
                             html.A('www.windhamcentral.org', 
                                    href='www.windhamcentral.org')]),
                ]),
            ], label='Tab 2')
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col('Column 1',width=2),
            dbc.Col('Column 2', width =5),
            dbc.Col('Column 3',width=4),
                ])
    ])
    
    # Initialize Dash app callbacks
    # init_callbacks(dash_app)
