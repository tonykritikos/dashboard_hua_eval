import dash
from dash import dcc
from dash import html
from dash import dash_table
import mysql.connector
import pandas as pd
import plotly.express as px
import config
import numpy as np
import warnings

from credentials import credential

connection = mysql.connector.connect(host=credential.host, database=credential.database, user=credential.user,
                                     password=credential.password)


# connection = mysql.connector.connect(host=input("Provide the host: "), database=input("Provide the database: "),
#                                      user=input("Provide the user: "), password=input("Provide the password: "))


def sql_query(command):
    cursor = connection.cursor()
    cursor.execute(command)
    dt = cursor.fetchall()
    cursor.close()
    return dt


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
a = np.array([np.NaN, np.NaN])
b = np.array([np.NaN, np.NaN, 3])

with warnings.catch_warnings():
    warnings.filterwarnings('error')
    try:
        x = np.nanmean(a)
    except RuntimeWarning:
        x = np.NaN
print(x)

df = pd.DataFrame(sql_query('select * from evaluation as unp;'), columns=config.columns)
courses = sql_query('select coursename, courseid from courses as unp;')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([

    dcc.Dropdown(
        id='course-dropdown',
        options=[
            {'label': i, 'value': y} for i, y in courses
        ],
        value=8,
        multi=False,
        clearable=False,
        style={'width': '80%'}
    ),

    html.Div(id='course-dropdown-output'),

    dcc.Dropdown(
        id='year-dropdown',
        options=[
            {'label': i, 'value': i} for i in range(1990, config.year + 1)
        ],
        value=2016,
        multi=False,
        clearable=False,
        style={'width': '80%'}
    ),

    html.Div(id='year-dropdown-output'),

    dcc.Tabs([
        dcc.Tab(children=[
            dcc.Graph(id='graph-q1_attendslectures', style={'width': '50%'}),
            dcc.Graph(id='graph-q2b_attendslabs', style={'width': '50%'}),
            dcc.Graph(id='graph-q14_evaluationcriteria', style={'width': '50%'}),
            dash_table.DataTable(
                id='datatable',
                columns=[{"name": 'opencomments', "id": 'opencomments'}]
            )
        ], id='tab1', label='Φοιτητής'),
        dcc.Tab(children=[
            dcc.Graph(id='graph-q2_coursehaslabs', style={'width': '50%'}),
            dcc.Graph(id='graph-q3_cleargoalslectures', style={'width': '50%'}),
            dcc.Graph(id='graph-q4_cleargoalslabs', style={'width': '50%'}),
            dcc.Graph(id='graph-q5_studymaterial', style={'width': '50%'}),
            dcc.Graph(id='graph-q12_materialcovered', style={'width': '50%'})
        ], id='tab2', label='Μάθημα'),
        dcc.Tab(children=[
            dcc.Graph(id='graph-q6_tutorinteresting', style={'width': '50%'}),
            dcc.Graph(id='graph-q7_tutorquestions', style={'width': '50%'}),
            dcc.Graph(id='graph-q8_tutorreachable', style={'width': '50%'}),
            dcc.Graph(id='graph-q9_tutorexplains', style={'width': '50%'}),
            dcc.Graph(id='graph-q10_tutorontime', style={'width': '50%'}),
            dcc.Graph(id='graph-q11_hasassistant', style={'width': '50%'}),
            dcc.Graph(id='graph-q11b_assistanthelps', style={'width': '50%'}),
            dcc.Graph(id='graph-q13_tutororganised', style={'width': '50%'})
        ], id='tab3', label='Καθηγητής'),
        dcc.Tab(children=[
            dcc.Dropdown(
                id='median-column',
                options=[
                    {'label': i, 'value': i} for i in config.median_columns
                ],
                value="q3_cleargoalslectures",
                multi=False,
                clearable=False,
                style={'width': '80%'}
            ),

            dcc.Graph(id='graph-median', style={'width': '50%'})
        ], id='tab4', label='Πορεία μαθήματος'),

        dcc.Tab(children=[
            dash_table.DataTable(
                id='year-rank-table',
                columns=[{'name': 'Course', 'id': 'courseid'}, {'name': 'Mean', 'id': 'Mean'}],
                style_cell=dict(textAlign='left'),
                style_header=dict(backgroundColor="paleturquoise"),
                style_data=dict(backgroundColor="lavender")
            )
        ], id='tab5', label='Κατάταξη')
    ]),
    html.Div(id='tabs')

])


@app.callback(
    dash.dependencies.Output('graph-q1_attendslectures', 'figure'),
    dash.dependencies.Output('graph-q2_coursehaslabs', 'figure'),
    dash.dependencies.Output('graph-q2b_attendslabs', 'figure'),
    dash.dependencies.Output('graph-q3_cleargoalslectures', 'figure'),
    dash.dependencies.Output('graph-q4_cleargoalslabs', 'figure'),
    dash.dependencies.Output('graph-q5_studymaterial', 'figure'),
    dash.dependencies.Output('graph-q6_tutorinteresting', 'figure'),
    dash.dependencies.Output('graph-q7_tutorquestions', 'figure'),
    dash.dependencies.Output('graph-q8_tutorreachable', 'figure'),
    dash.dependencies.Output('graph-q9_tutorexplains', 'figure'),
    dash.dependencies.Output('graph-q10_tutorontime', 'figure'),
    dash.dependencies.Output('graph-q11_hasassistant', 'figure'),
    dash.dependencies.Output('graph-q11b_assistanthelps', 'figure'),
    dash.dependencies.Output('graph-q12_materialcovered', 'figure'),
    dash.dependencies.Output('graph-q13_tutororganised', 'figure'),
    dash.dependencies.Output('graph-q14_evaluationcriteria', 'figure'),
    dash.dependencies.Output('graph-median', 'figure'),
    [dash.dependencies.Input('course-dropdown', 'value'),
     dash.dependencies.Input('median-column', 'value'),
     dash.dependencies.Input('year-dropdown', 'value')])
def update_data(courseid, median_column, syear):
    dff = df[(df['courseid'] == courseid) & (df['qyear'] == syear)]
    piechart1 = px.pie(dff, names='q1_attendslectures', hole=.0, title='Παρακολούθησαν το μάθημα')
    piechart2 = px.pie(dff, names='q2_coursehaslabs', hole=.0, title='Έχει το μάθημα εργαστήρια')
    piechart3 = px.pie(dff, names='q2b_attendslabs', hole=.0, title='Παρακολουθεί τα εργαστήρια')
    barchart4 = px.bar(dff, x="q3_cleargoalslectures", title="Επιτυγχάνει τους στόχους στις διαλέξεις")
    barchart5 = px.bar(dff, x="q4_cleargoalslabs", title="Επιτυγχάνει τους στόχους στα εργαστήρια")
    barchart6 = px.bar(dff, x="q5_studymaterial", title="Υλικό μαθήματος")
    barchart7 = px.bar(dff, x="q6_tutorinteresting", title="Είναι ενδιαφέρων ο/η καθηγητής/τρια")
    barchart8 = px.bar(dff, x="q7_tutorquestions", title="Απαντάει σε ερωτήσεις")
    barchart9 = px.bar(dff, x="q8_tutorreachable", title="Είναι εύκολα προσβάσιμος/η")
    barchart10 = px.bar(dff, x="q9_tutorexplains", title="Εξηγεί καλά")
    barchart11 = px.bar(dff, x="q10_tutorontime", title="Είναι στην ώρα του")
    piechart12 = px.pie(dff, names='q11_hasassistant', hole=.0, title='Έχει βοηθό')
    barchart13 = px.bar(dff, x="q11b_assistanthelps", title="Κατά πόσο ο βοηθός βοηθάει")
    barchart14 = px.bar(dff, x="q12_materialcovered", title="Καλύπτεται το υλικό")
    barchart15 = px.bar(dff, x="q13_tutororganised", title="Είναι οργανωμένος/η")
    barchart16 = px.bar(dff, x="q14_evaluationcriteria", title="Κριτήρια αξιολόγησης")

    mean_df = df[(df['courseid'] == courseid)]
    barchart17 = px.line(mean_df[config.median_columns_plus_year].groupby(['qyear']).mean(), y=median_column,
                         title="Μέσος όρος ανά χρονιά")

    return piechart1, piechart2, piechart3, barchart4, barchart5, barchart6, barchart7, barchart8, barchart9, \
           barchart10, barchart11, piechart12, barchart13, barchart14, barchart15, barchart16, barchart17


@app.callback(
    dash.dependencies.Output('datatable', 'data'),
    [dash.dependencies.Input('course-dropdown', 'value'),
     dash.dependencies.Input('year-dropdown', 'value')])
def comment_table(courseid, syear):
    data_df = df[(df['courseid'] == courseid) & (df['qyear'] == syear)]
    return data_df.dropna(subset=['opencomments']).to_dict('records')


@app.callback(
    dash.dependencies.Output('year-rank-table', 'data'),
    [dash.dependencies.Input('year-dropdown', 'value')])
def year_list(syear):
    year_medians = df[(df['qyear'] == syear)]
    year_medians['Mean'] = year_medians.loc[:, config.median_columns].mean(axis=1, skipna=True)
    for name, number in courses:
        year_medians['courseid'] = year_medians['courseid'].replace(number, name)
    return year_medians.groupby(['courseid'], as_index=False).mean().sort_values('Mean', ascending=False).to_dict(
        'records')



connection.close()

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8050, debug=True)
