# from dash_app import init_dashboard as da
# from dash import Dash, dash_table, dcc, html, Input, Output, callback, State



# def get_callbacks(da):
#     @da.callback(
#         Output('test-par-data-entry', 'children'),
#         Input('submit', 'n_clicks'),
#         State('table-editing', 'data'),
#         prevent_initial_call=True)
    
#     def update_table(n_clicks, data):
#     # Check if the "Submit" button has been clicked
#         if n_clicks is not None:
#             # Get the current state of the DataTable component
#             current_data = data

#             # Perform any additional logic here to update the table based on the current state of the DataTable component

#             # Return the updated table data
#             return html.Div(children=current_data)
#         else:
#             # If the "Submit" button has not been clicked, return the original table data
#             return html.Div(children=data)
#     return update_table