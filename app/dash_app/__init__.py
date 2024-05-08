# from dash import Dash, dash_table, dcc, html, Input, Output, callback, State
# from flask import Flask
# from flask_login import login_required, current_user
# import dash_bootstrap_components as dbc
# from dash.dependencies import Output, Input
# import plotly.express as px
# import pandas as pd
# from models import *
# from .literacy_par import lit_layout
# from call_backs import get_callbacks

# def init_dashboard(server):
#     dash_app = Dash(
#         server=server,
#         routes_pathname_prefix='/dash/',
#         external_stylesheets=[dbc.themes.LITERA]
#     )

#     dash_app.layout = literacy_par.lit_layout
#     get_callbacks(dash_app)

#     if __name__ == '__main__':
#         dash_app.run_server(debug=True)

#     return dash_app.server



