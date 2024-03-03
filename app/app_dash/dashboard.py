# app_dash/dashboard.py
import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input 
from db_util import *
from models import db

    

def init_admin_dashboard(server):
    # Create Dash app instance
    dash_app = dash.Dash(server=server, routes_pathname_prefix='/dash/', external_stylesheets=[dbc.themes.LITERA])
    
    def plot_lit_scores():
        query = str(f'SELECT * FROM v_detailed_lit_scores')
        result = pd.read_sql(query, con=db.session)
        return result
    
    df = plot_lit_scores()
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
        dbc.Container([
            dbc.Label('Click a cell in the table:'),
            dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]),
            dbc.Alert(id='tbl_out'),
        ]),
                
        dbc.Row([
            dbc.Col('Column 1',width=2),
            dbc.Col('Column 2', width =5),
            dbc.Col('Column 3',width=4),
                ])
    ])
    
    # Initialize Dash app callbacks
    
    @callback(Output('tbl_out', 'children'), Input('tbl', 'active_cell'))
    def update_graphs(active_cell):
        return str(active_cell) if active_cell else "Click the table"
    # init_callbacks(dash_app)

