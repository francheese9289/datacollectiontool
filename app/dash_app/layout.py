

# def basic_layout(dash_app):
#     colors = {
#     'background': '#111111',
#     'text': '#7FDBFF'
#     }
#     #fake/example data
#     df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
#     })

#     fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

#     fig.update_layout(
#         plot_bgcolor=colors['background'],
#         paper_bgcolor=colors['background'],
#         font_color=colors['text']
#     )
#     #basic layout/ component examples
#     dash_app.layout = html.Div(#style={'backgroundColor': colors['background']}, children=[
#             html.H1(children='Dashboard',
#             style={
#             'textAlign': 'center',
#             'color': colors['text']
#         }), # Each component is described entirely through keyword attributes. Dash is declarative: you will primarily describe your app through these attributes.
#             html.Div([
#                 html.H2('Literacy Assessments'),
#                  dbc.Tab([
#                      dbc.Tabs([
#                          html.Ul([
#                              html.Li('Predictive Assessment of Reading'),
#                              html.Li('Words Their Way'),
#                              html.Li('AimsWeb Upload')
#                          ])
#                      ])
#                  ])]))
#         #           children='''
#         #              Example dash layout
#         #              ''', style={
#         #             'textAlign': 'center',
#         #             'color': colors['text']
#         # }),
#         #     dcc.Graph(
#         #     id='example-graph',
#         #     figure=fig
#         #     )
#         # ])
                
#     return dash_app.layout




# def basic_table(dash_app):
#     params = [
#     'Weight', 'Torque', 'Width', 'Height',
#     'Efficiency', 'Power', 'Displacement'
# ]

#     dash_app.layout = html.Div([
#         dash_table.DataTable(
#             id='table-editing-simple',
#             columns=(
#                 [{'id': 'Model', 'name': 'Model'}] +
#                 [{'id': p, 'name': p} for p in params]
#             ),
#             data=[
#                 dict(Model=i, **{param: 0 for param in params})
#                 for i in range(1, 5)
#             ],
#             editable=True
#         ),
#         dcc.Graph(id='table-editing-simple-output')
# ])


# @callback(
#     Output('table-editing-simple-output', 'figure'),
#     Input('table-editing-simple', 'data'),
#     Input('table-editing-simple', 'columns'))
# def display_output(rows, columns):
#     df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
#     return {
#         'data': [{
#             'type': 'parcoords',
#             'dimensions': [{
#                 'label': col['name'],
#                 'values': df[col['id']]
#             } for col in columns]
#         }]
#     }


# # # def init_callbacks(dash_app):
# # #     @dash_app.callback(
# # #     # Callback input/output
# # #     ....
# # #     )
# # #     def update_graph(rows):
# # #         # Callback logic
# #         # ...


# # @login_required
# # def my_first_layout(dash_app, assessment = 'Predictive Assessment of Reading'):
# #     '''attempting to create an editable form!'''
# #     components = data_entry()

# #     dash_app.layout = html.Div([
# #         dash_table.DataTable(
# #             id='table-editing-simple',
# #             columns=(
# #                 [{'id': 'Student', 'name': 'Student Name'}] +
# #                 [{'id': c, 'name': c} for c in components]
# #             ),
# #             data=[
# #                 dict(Model=i, **{comp: 0 for comp in components})
# #                 for i in range(1, 5)
# #             ],
# #             editable=True
# #         ),
# #         dcc.Graph(id='table-editing-simple-output')
# #     ])


# #     @callback(
# #         Output('table-editing-simple-output', 'figure'),
# #         Input('table-editing-simple', 'data'),
# #         Input('table-editing-simple', 'columns'))
    
# #     def display_output(rows, columns):
# #         df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
# #         return {
# #             'data': [{
# #                 'type': 'parcoords',
# #                 'dimensions': [{
# #                     'label': col['name'],
# #                     'values': df[col['id']]
# #                 } for col in columns]
# #             }]
# #         }
