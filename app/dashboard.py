import dash
from dash import dcc
from dash import html
from dash import dash_table
import mysql.connector
import pandas as pd
import plotly.express as px
import datetime
# from credentials import credential
#
# connection = mysql.connector.connect(host=credential.host, database=credential.database, user=credential.user,
#                                      password=credential.password)
host = input("Provide the host: ")
# print(host)
database = input("Provide the database: ")
# print(database)
user = input("Provide the user: ")
# print(user)
password = input("Provide the password: ")
# print(password)
connection = mysql.connector.connect(host=host, database=database, user=user,
                                     password=password)


def sql_query(command):
    cursor = connection.cursor()
    cursor.execute(command)
    dt = cursor.fetchall()
    cursor.close()
    return dt


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

columns = ['qid', 'qlastpage', 'q1_attendslectures', 'q2_coursehaslabs', 'q2b_attendslabs',
           'q3_cleargoalslectures', 'q4_cleargoalslabs', 'q5_studymaterial',
           'q6_tutorinteresting',
           'q7_tutorquestions', 'q8_tutorreachable', 'q9_tutorexplains',
           'q10_tutorontime', 'q11_hasassistant', 'q11b_assistanthelps',
           'q12_materialcovered',
           'q13_tutororganised', 'q14_evaluationcriteria', 'opencomments', 'courseid',
           'qyear', 'qseason']

df = pd.DataFrame(sql_query('select * from evaluation as unp;'), columns=columns)
courses = sql_query('select coursename, courseid from courses as unp;')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True

year = int((datetime.datetime.now().strftime('%Y')))

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
            {'label': i, 'value': i} for i in range(1990, year + 1)
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
            dcc.Graph(id='graph-q14_evaluationcriteria', style={'width': '50%'})
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
        ], id='tab3', label='Καθηγητής')
    ]),
    html.Div(id='tabs'),

    dash_table.DataTable(
        id='datatable',
        columns=[{"name": 'opencomments', "id": 'opencomments'}]
    ),
    html.Div(id='datatable-output')
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
    [dash.dependencies.Input('course-dropdown', 'value'),
     dash.dependencies.Input('year-dropdown', 'value')])
def update_data(courseid, syear):
    dff = df[(df['courseid'] == courseid) & (df['qyear'] == syear)]
    piechart1 = px.pie(dff, names='q1_attendslectures', hole=.0, title='Παρακολούθησαν το μάθημα')
    piechart2 = px.pie(dff, names='q2_coursehaslabs', hole=.0, title='Έχει το μάθημα εργαστήρια')
    piechart3 = px.pie(dff, names='q2b_attendslabs', hole=.0, title='Παρακολουθεί τα εργαστήρια')
    barchart4 = px.bar(dff, x="q3_cleargoalslectures", title="q3_cleargoalslectures")
    barchart5 = px.bar(dff, x="q4_cleargoalslabs", title="q4_cleargoalslabs")
    barchart6 = px.bar(dff, x="q5_studymaterial", title="q5_studymaterial")
    barchart7 = px.bar(dff, x="q6_tutorinteresting", title="q6_tutorinteresting")
    barchart8 = px.bar(dff, x="q7_tutorquestions", title="q7_tutorquestions")
    barchart9 = px.bar(dff, x="q8_tutorreachable", title="q8_tutorreachable")
    barchart10 = px.bar(dff, x="q9_tutorexplains", title="q9_tutorexplains")
    barchart11 = px.bar(dff, x="q10_tutorontime", title="q10_tutorontime")
    piechart12 = px.pie(dff, names='q11_hasassistant', hole=.0, title='Έχει βοηθό')
    barchart13 = px.bar(dff, x="q11b_assistanthelps", title="q11b_assistanthelps")
    barchart14 = px.bar(dff, x="q12_materialcovered", title="q12_materialcovered")
    barchart15 = px.bar(dff, x="q13_tutororganised", title="q13_tutororganised")
    barchart16 = px.bar(dff, x="q14_evaluationcriteria", title="q14_evaluationcriteria")
    return piechart1, piechart2, piechart3, barchart4, barchart5, barchart6, barchart7, barchart8, barchart9,\
           barchart10, barchart11, piechart12, barchart13, barchart14, barchart15, barchart16


@app.callback(
    dash.dependencies.Output('datatable', 'data'),
    [dash.dependencies.Input('course-dropdown', 'value'),
     dash.dependencies.Input('year-dropdown', 'value')])
def data_table(courseid, syear):
    data_df = df[(df['courseid'] == courseid) & (df['qyear'] == syear)]
    return data_df.dropna(subset=['opencomments']).to_dict('records')


connection.close()

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
