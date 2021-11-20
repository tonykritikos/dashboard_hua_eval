import textwrap

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
from plotly.graph_objects import Layout
from plotly.validator_cache import ValidatorCache

from credentials import credential

connection = mysql.connector.connect(host=credential.host, database=credential.database, user=credential.user,
                                     password=credential.password)


# connection = mysql.connector.connect(host=input("Provide the host: "), database=input("Provide the database: "),
#                                      user=input("Provide the user: "), password=input("Provide the password: "))

# Query that runs the scripts to take the courses and the data
def sql_query(command):
    cursor = connection.cursor()
    cursor.execute(command)
    dt = cursor.fetchall()
    cursor.close()
    return dt


# Start of block  that suppresses errors
a = np.array([np.NaN, np.NaN])
b = np.array([np.NaN, np.NaN, 3])

with warnings.catch_warnings():
    warnings.filterwarnings('error')
    try:
        x = np.nanmean(a)
    except RuntimeWarning:
        x = np.NaN
print(x)
pd.options.mode.chained_assignment = None  # default='warn'
# End of block that suppresses errors

df = pd.DataFrame(sql_query('select * from evaluation as unp;'), columns=config.columns)  # Main dataframe call
courses = sql_query('select coursename, courseid from courses as unp;')  # Courses

# Start of styling and configuration block
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True
# End of styling and configuration block

# Start of the main layout app
app.layout = html.Div([

    dcc.Dropdown(
        id='course-dropdown',  # Main dropdown - Courses
        options=[
            {'label': i, 'value': y} for i, y in courses
        ],
        value=8,  # Assigned default value so when it loads it instantly shows data
        multi=False,
        clearable=False,
        style={'width': '60%'}
    ),

    html.Div(id='course-dropdown-output'),

    dcc.Dropdown(
        id='year-dropdown',  # Main dropdown - Year
        options=[
            {'label': i, 'value': i} for i in range(1990, config.year + 1)
        ],  # The range of the years is HUA established year (1990) to current year
        value=2016,  # Assigned default value so when it loads it instantly shows data
        multi=False,
        clearable=False,
        style={'width': '60%'}
    ),

    html.Div(id='year-dropdown-output'),

    dcc.Tabs([
        dcc.Tab(children=[  # First tab - Student
            dcc.Graph(id='graph-q1_attendslectures', style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(id='graph-q2b_attendslabs', style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(id='graph-q14_evaluationcriteria', style={'width': '50%', 'display': 'inline-block'}),
            dash_table.DataTable(
                id='datatable',
                columns=[{"name": config.titles('opencomments'), "id": 'opencomments'}],
                style_cell={'textAlign': 'center', 'height': '25px'},
                style_header={'fontWeight': 'bold'},
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto'},
                style_table={'max-width': '50%', 'margin-left': '50%','margin-top': '-65vh','word-wrap': 'break-word'}
            )
        ], id='tab1', label='Φοιτητής'),
        dcc.Tab(children=[  # Second tab - Lesson
            dcc.Graph(id='graph-q2_coursehaslabs', style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(id='graph-q3_cleargoalslectures', style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(id='graph-q4_cleargoalslabs', style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(id='graph-q5_studymaterial', style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(id='graph-q12_materialcovered', style={'width': '50%', 'display': 'inline-block'})
        ], id='tab2', label='Μάθημα'),
        dcc.Tab(children=[  # Third tab - Professor and tutor
            dcc.Graph(id='graph-q6_tutorinteresting', style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(id='graph-q7_tutorquestions', style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(id='graph-q8_tutorreachable', style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(id='graph-q9_tutorexplains', style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(id='graph-q10_tutorontime', style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(id='graph-q11_hasassistant', style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(id='graph-q11b_assistanthelps', style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(id='graph-q13_tutororganised', style={'width': '50%', 'display': 'inline-block'})
        ], id='tab3', label='Καθηγητής'),
        dcc.Tab(children=[  # Fourth tab - Average score per numeric column for the selected lesson through the years
            dcc.Dropdown(
                id='mean-column',  # Inner dropdown - Select column to show the average score
                options=[
                    {'label': i, 'value': y} for y, i in config.dict_mean_columns
                ],
                value="q3_cleargoalslectures",  # Assigned default value so when it loads it instantly shows data
                multi=False,
                clearable=False,
                style={'width': '80%'}
            ),

            dcc.Graph(id='graph-mean', style={'width': '50%', 'display': 'inline-block'})
        ], id='tab4', label='Πορεία μαθήματος'),

        dcc.Tab(children=[  # Fifth tab - List of average overall score of each lesson, ranked most to least
            dash_table.DataTable(
                id='year-rank-table',
                columns=[{'name': 'Μάθημα', 'id': 'courseid'}, {'name': 'Μέσος Όρος', 'id': 'Mean'}],
                style_cell=dict(textAlign='center'),
                style_table={'width': '70%', 'display': 'inline-block'}
            )
        ], id='tab5', label='Κατάταξη')
    ]),
    html.Div(id='tabs')

])


@app.callback(
    dash.dependencies.Output('graph-q1_attendslectures', 'figure'),
    dash.dependencies.Output('graph-q2b_attendslabs', 'figure'),
    dash.dependencies.Output('graph-q14_evaluationcriteria', 'figure'),
    dash.dependencies.Output('datatable', 'data'),
    [dash.dependencies.Input('course-dropdown', 'value'),
     dash.dependencies.Input('year-dropdown', 'value')])
def first_tab(courseid, syear):
    first_tab_df = df[(df['courseid'] == courseid) & (df['qyear'] == syear)]
    piechart1 = px.pie(first_tab_df.dropna(subset=['q1_attendslectures']), names='q1_attendslectures', hole=.0,
                       title=config.titles('q1_attendslectures'))
    piechart2 = px.pie(first_tab_df.dropna(subset=['q2b_attendslabs']), names='q2b_attendslabs', hole=.0,
                       title=config.titles('q2b_attendslabs'))
    barchart = px.bar(first_tab_df['q14_evaluationcriteria'], title=config.titles('q14_evaluationcriteria'),
                      labels=config.bar_labels, range_x=config.bar_x_range,
                      height=config.height, width=config.width, barmode='relative')
    return piechart1, piechart2, barchart.update_layout(showlegend=False), first_tab_df.dropna(subset=['opencomments']).to_dict('records')


@app.callback(
    dash.dependencies.Output('graph-q2_coursehaslabs', 'figure'),
    dash.dependencies.Output('graph-q3_cleargoalslectures', 'figure'),
    dash.dependencies.Output('graph-q4_cleargoalslabs', 'figure'),
    dash.dependencies.Output('graph-q5_studymaterial', 'figure'),
    dash.dependencies.Output('graph-q12_materialcovered', 'figure'),
    [dash.dependencies.Input('course-dropdown', 'value'),
     dash.dependencies.Input('year-dropdown', 'value')])
def second_tab(courseid, syear):
    second_tab_df = df[(df['courseid'] == courseid) & (df['qyear'] == syear)]
    piechart = px.pie(second_tab_df.dropna(subset=['q2_coursehaslabs']), names='q2_coursehaslabs', hole=.0,
                      title=config.titles('q2_coursehaslabs'))
    barchart1 = px.bar(second_tab_df['q3_cleargoalslectures'], title=config.titles('q3_cleargoalslectures'),
                       labels=config.bar_labels, range_x=config.bar_x_range,
                       height=config.height, width=config.width, barmode='relative')
    barchart2 = px.bar(second_tab_df['q4_cleargoalslabs'], title=config.titles('q4_cleargoalslabs'),
                       labels=config.bar_labels, range_x=config.bar_x_range,
                       height=config.height, width=config.width, barmode='relative')
    barchart3 = px.bar(second_tab_df['q5_studymaterial'], title=config.titles('q5_studymaterial'),
                       labels=config.bar_labels, range_x=config.bar_x_range,
                       height=config.height, width=config.width, barmode='relative')
    barchart4 = px.bar(second_tab_df['q12_materialcovered'], title=config.titles('q12_materialcovered'),
                       labels=config.bar_labels, range_x=config.bar_x_range,
                       height=config.height, width=config.width, barmode='relative')
    return piechart, barchart1.update_layout(showlegend=False), barchart2.update_layout(
        showlegend=False), barchart3.update_layout(showlegend=False), barchart4.update_layout(showlegend=False)


@app.callback(
    dash.dependencies.Output('graph-q6_tutorinteresting', 'figure'),
    dash.dependencies.Output('graph-q7_tutorquestions', 'figure'),
    dash.dependencies.Output('graph-q8_tutorreachable', 'figure'),
    dash.dependencies.Output('graph-q9_tutorexplains', 'figure'),
    dash.dependencies.Output('graph-q10_tutorontime', 'figure'),
    dash.dependencies.Output('graph-q11_hasassistant', 'figure'),
    dash.dependencies.Output('graph-q11b_assistanthelps', 'figure'),
    dash.dependencies.Output('graph-q13_tutororganised', 'figure'),
    [dash.dependencies.Input('course-dropdown', 'value'),
     dash.dependencies.Input('year-dropdown', 'value')])
def third_tab(courseid, syear):
    third_tab_df = df[(df['courseid'] == courseid) & (df['qyear'] == syear)]
    barchart1 = px.bar(third_tab_df['q6_tutorinteresting'], title=config.titles('q6_tutorinteresting'),
                       labels=config.bar_labels, range_x=config.bar_x_range,
                       height=config.height, width=config.width, barmode='relative')
    barchart2 = px.bar(third_tab_df['q7_tutorquestions'], title=config.titles('q7_tutorquestions'),
                       labels=config.bar_labels, range_x=config.bar_x_range,
                       height=config.height, width=config.width, barmode='relative')
    barchart3 = px.bar(third_tab_df['q8_tutorreachable'], title=config.titles('q8_tutorreachable'),
                       labels=config.bar_labels, range_x=config.bar_x_range,
                       height=config.height, width=config.width, barmode='relative')
    barchart4 = px.bar(third_tab_df['q9_tutorexplains'], title=config.titles('q9_tutorexplains'),
                       labels=config.bar_labels, range_x=config.bar_x_range,
                       height=config.height, width=config.width, barmode='relative')
    barchart5 = px.bar(third_tab_df['q10_tutorontime'], title=config.titles('q10_tutorontime'),
                       labels=config.bar_labels, range_x=config.bar_x_range,
                       height=config.height, width=config.width, barmode='relative')
    piechart = px.pie(third_tab_df.dropna(subset=['q11_hasassistant']), names='q11_hasassistant', hole=.0,
                      title=config.titles('q11_hasassistant'))
    barchart6 = px.bar(third_tab_df['q11b_assistanthelps'], title=config.titles('q11b_assistanthelps'),
                       labels=config.bar_labels, range_x=config.bar_x_range,
                       height=config.height, width=config.width, barmode='relative')
    barchart7 = px.bar(third_tab_df['q13_tutororganised'], title=config.titles('q13_tutororganised'),
                       labels=config.bar_labels, range_x=config.bar_x_range,
                       height=config.height, width=config.width, barmode='relative')
    return barchart1.update_layout(showlegend=False), barchart2.update_layout(
        showlegend=False), barchart3.update_layout(showlegend=False), barchart4.update_layout(
        showlegend=False), barchart5.update_layout(showlegend=False), piechart, barchart6.update_layout(
        showlegend=False), barchart7.update_layout(
        showlegend=False)


@app.callback(
    dash.dependencies.Output('graph-mean', 'figure'),
    [dash.dependencies.Input('course-dropdown', 'value'),
     dash.dependencies.Input('mean-column', 'value')])
def fourth_tab(courseid, mean_column):
    fourth_tab_df = df[(df['courseid'] == courseid)]
    barchart = px.line(fourth_tab_df[config.mean_columns_plus_year].groupby(['qyear']).mean(), y=mean_column,
                       title="Μέσος όρος", height=config.height, width=config.width)
    return barchart.update_xaxes(dtick=1).update_layout(xaxis_title="Έτος", yaxis_title="Μέσος όρος", showlegend=False)


@app.callback(
    dash.dependencies.Output('year-rank-table', 'data'),
    [dash.dependencies.Input('year-dropdown', 'value')])
def fifth_tab(syear):
    fifth_tab_df = df[(df['qyear'] == syear)]
    fifth_tab_df['Mean'] = fifth_tab_df.loc[:, config.mean_columns].mean(axis=1, skipna=True)
    for name, number in courses:
        fifth_tab_df['courseid'] = fifth_tab_df['courseid'].replace(number, name)
    return fifth_tab_df.groupby(['courseid'], as_index=False).mean().round(2).sort_values('Mean',
                                                                                          ascending=False).to_dict(
        'records')


connection.close()

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8050, debug=True)
