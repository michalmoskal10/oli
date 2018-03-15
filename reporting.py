import dash
import os

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
import plotly.graph_objs as go
from plotly.graph_objs import *
import dash_auth



with open('.pass') as f:
    VALID_USERNAME_PASSWORD_PAIRS = [x.strip().split(':') for x in f.readlines()]

files_videos = {
    'Week1': 'data/week1.csv',
    'Week2': 'data/week2.csv',
    'Week3': 'data/week3.csv',
    'Week4': 'data/week4.csv',
    'all': 'data/all.csv'
}

files_assignments = {
    'Week1': 'data/week1_assignments.csv',
    'Week2': 'data/week2_assignments.csv',
    'Week3': 'data/week3_assignments.csv',
    'Week4': 'data/week4_assignments.csv',
    'all': 'data/all_ass.csv'
}

files_assignments_table = {
    'Week1': 'data/week1_assignments_table.csv',
    'Week2': 'data/week2_assignments_table.csv',
    'Week3': 'data/week3_assignments_table.csv',
    'Week4': 'data/week4_assignments_table.csv',
    'all': 'data/assignments_table.csv'
}

active_users = {
    'Week1':1338,
    'Week2':648,
    'Week3':351,
    'Week4':303,
    'all': 1646
}

DF_GAPMINDER = pd.read_csv(
    'data/assignments_table.csv'
    #'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv'
)
#DF_GAPMINDER = DF_GAPMINDER[DF_GAPMINDER['year'] == 2007]

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'c78bf172206ce24f77d6363a2d754b59/raw/'
    'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
    'usa-agricultural-exports-2011.csv')

app = dash.Dash('auth')
server = app.server
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div([
    html.H4('Robotics: Aerial Robotics'),


    #html.Div(id='selected-indexes'),

    html.Div(children=[
            html.Label('Session'),
            dcc.Dropdown(
                id='session',
                options=[
                    {'label': '2016-01-15 - 2016-02-22', 'value': 1},
                    {'label': '2016-02-15 - 2016-03-21', 'value': 2},
                    {'label': '2016-03-14 - 2016-04-18', 'value': 3},
                    {'label': '2016-04-11 - 2016-05-16', 'value': 4},
                    {'label': '2016-05-09 - 2016-06-13', 'value': 5},
                    {'label': '2016-06-06 - 2016-07-11', 'value': 6},
                    {'label': '2016-07-04 - 2016-08-08', 'value': 7},
                    {'label': '2016-08-01 - 2016-09-05', 'value': 8},
                    {'label': '2016-08-29 - 2016-10-03', 'value': 9},
                    {'label': '2016-09-26 - 2016-10-31', 'value': 10},
                    {'label': '2016-09-26 - 2016-10-31', 'value': 11},
                    {'label': '2016-09-26 - 2016-10-31', 'value': 12},
                    {'label': '2016-10-24 - 2016-11-28', 'value': 13},
                    {'label': '2016-10-24 - 2016-11-28', 'value': 14},
                    {'label': '2016-10-24 - 2016-11-28', 'value': 15},
                    {'label': '2016-11-21 - 2016-12-26', 'value': 16},
                    {'label': '2016-11-21 - 2016-12-26', 'value': 17},
                    {'label': '2016-11-21 - 2016-12-26', 'value': 18},
                    {'label': '2016-12-19 - 2017-01-23', 'value': 19},
                    {'label': '2016-12-19 - 2017-01-23', 'value': 20},
                    {'label': '2016-12-19 - 2017-01-23', 'value': 21},
                    {'label': '2017-01-09 - 2017-04-24', 'value': 22},
                    {'label': '2017-01-16 - 2017-02-20', 'value': 23},
                    {'label': '2017-02-13 - 2017-03-20', 'value': 24},
                    {'label': '2017-03-13 - 2017-04-17', 'value': 25},
                    {'label': '2017-04-10 - 2017-05-15', 'value': 26},
                    {'label': '2017-05-08 - 2017-06-12', 'value': 27},
                    {'label': '2017-06-05 - 2017-07-10', 'value': 28},
                    {'label': '2017-07-03 - 2017-08-07', 'value': 29},
                    {'label': '2017-07-31 - 2017-09-04', 'value': 30},
                    {'label': '2017-08-28 - 2017-10-02', 'value': 31},
                    {'label': '2017-09-25 - 2017-10-30', 'value': 32},
                    {'label': '2017-10-23 - 2017-11-27', 'value': 33},
                    {'label': '2017-11-20 - 2017-12-25', 'value': 34},
                    {'label': '2017-12-18 - 2018-01-22', 'value': 35},
                    {'label': '2018-01-15 - 2018-02-19', 'value': 36},
                ],
                value=36,
            ),],
        style={'marginBottom': 30, 'marginTop': 25, 'marginLeft': 100, 'marginRight':100}
    ),

    html.Div(children=[
        html.Label('Module'),
        dcc.Dropdown(
            id='module',
            options=[
                {'label': '1. Introduction to Aerial Robotics', 'value': 'Week1'},
                {'label': '2. Geometry and Mechanics', 'value': 'Week2'},
                {'label': '3. Planning and Control', 'value': 'Week3'},
                {'label': '4. Advanced Topics', 'value': 'Week4'},
                {'label': 'All modules', 'value': 'all'},

            ],
            value='Week1'
        ), ],
        style={'marginBottom': 50, 'marginLeft': 100, 'marginRight': 100}
    ),
    html.H6('Total number of students enrolled for this time period: 1242.', style={'margin-left': '70'}),
    html.H6('Total number of active students in this time period: 1646.', style={'margin-left': '70'}),
    html.H6('Number of students enrolled in previous sessions but active in current session: 1135.', style={'margin-left': '70'}),
    html.Div(
        children=[
            html.H3('% of ever-active users for whom video was the last video seen before dropping out of or completing the course.',
                    style={'text-align':'center',
                           'padding-bottom':'-1em'}),
            dcc.Graph(id='video_last_seen'),

        ],
        style={
            'marginLeft': 60,
            'marginRight': 60,
            'marginBottom': 90,
            'marginTop': 100
        },
    ),

    html.Div(
        children=[
            html.H2('% of students active in week who watched a video',
                    style={'text-align': 'center'}),
            dcc.Graph(id='watched'),

            html.Div(id='active_in_week')
        ],
        style={
            'marginLeft':60,
            'marginRight':60,
            'marginBottom': 90,
            'marginTop': 0
        }
    ),

    html.Div(
        children=[
            html.H3('% of time each assignment was last seen before dropping out of or completing the course.',
                    style={'text-align': 'center'}),
            dcc.Graph(id='assignment_last_seen'),

        ],
        style={
            'marginLeft': 60,
            'marginRight': 60,
            'marginBottom': 50,
            'marginTop': 0
        }
    ),
    html.Div(
        children=[
            dt.DataTable(
                rows=[{}],
                # optional - sets the order of columns
                columns = ['Course order', 'Assignment', 'Last seen (%)'],
                # columns=sorted(DF_GAPMINDER.columns),

                # filterable=True,
                sortable = True,
                selected_row_indices = [],
                id='assignments_table',
            )
        ],
        style={
            'marginLeft': 60,
            'marginRight': 60,
            'marginBottom': 50,
            'marginTop': 0
        }
    )



],
    className="container"
)

@app.callback(Output('video_last_seen', 'figure'), [Input('module', 'value')])
def update_graph(selected_dropdown_value):
    #df = web.DataReader(
    #    selected_dropdown_value, data_source='google',
    #    start=dt(2017, 1, 1), end=dt.now())
    df = pd.read_csv(files_videos[selected_dropdown_value])

    l = df['last_seen'].tolist()
    s = 1646

    if len(l) < 10:
        range = len(l) - 0.5
    else:
        range = 9.5
    return {
        # 'data': [{
        #     'x': df.index,
        #     'y': df.values,
        #     'type': 'bar'
        # }]
        'data': [go.Bar(
            x=df['video'].tolist(),
            y=[x/s for x in l]
        )],
        'layout':{
            #'autosize':True,
            'height':900,
            'width':900,
            'yaxis': {
                'tickformat': '%'
            },
            'xaxis': {
                'tickangle': 45,
                'range': [-0.5, range],

            },
            'annotations': Annotations([
                Annotation(
                    x=0.5004254919715793,
                    y=1.13191064079952971,
                    showarrow=False,
                    text='Left to right is order in the course',
                    xref='paper',
                    yref='paper'
                )
            ]),
            'margin': Margin(b=350)
        }
    }

@app.callback(Output('watched', 'figure'), [Input('module', 'value')])
def update_graph(selected_dropdown_value):
    #df = web.DataReader(
    #    selected_dropdown_value, data_source='google',
    #    start=dt(2017, 1, 1), end=dt.now())
    df = pd.read_csv(files_videos[selected_dropdown_value])
    s1 = active_users[selected_dropdown_value]

    l1 = df['watched'].tolist()
    if len(l1) < 10:
        range = len(l1) - 0.5
    else:
        range = 9.5
    return {
        # 'data': [{
        #     'x': df.index,
        #     'y': df.values,
        #     'type': 'bar'
        # }]
        'data': [go.Bar(
            x=df['video'].tolist(),
            y=[x/s1 for x in l1]
        )],
        'layout':{
            'height': 900,
            'width': 900,
            'yaxis': {

                'tickformat': '%'
            },
            'xaxis': {
                'tickangle': 45,
                'range': [-0.5, range],

            },
            'annotations': Annotations([
                Annotation(
                    x=0.5004254919715793,
                    y=1.13191064079952971,
                    showarrow=False,
                    text='Left to right is order in the course',
                    xref='paper',
                    yref='paper'
                )
            ]),
            'margin': Margin(b=350)
        }
    }

@app.callback(Output('assignment_last_seen', 'figure'), [Input('module', 'value')])
def update_graph(selected_dropdown_value):
    #df = web.DataReader(
    #    selected_dropdown_value, data_source='google',
    #    start=dt(2017, 1, 1), end=dt.now())
    df3 = pd.read_csv(files_assignments[selected_dropdown_value])


    l3 = df3['last_seen'].tolist()
    s3 = 896


    return {
        # 'data': [{
        #     'x': df.index,
        #     'y': df.values,
        #     'type': 'bar'
        # }]
        'data':[go.Bar(
            x=df3['name'].tolist(),
            y=[x / s3 for x in l3]
        )],
        'layout': {
            'yaxis': {
                'tickformat': '%'
            },
            'annotations': Annotations([
                Annotation(
                    x=0.5004254919715793,
                    y=1.13191064079952971,
                    showarrow=False,
                    text='Left to right is order in the course',
                    xref='paper',
                    yref='paper'
                )
            ])
        }
    }


@app.callback(Output('assignments_table', 'rows'), [Input('module', 'value')])
def update_graph(selected_dropdown_value):
    df5 = pd.read_csv(files_assignments_table[selected_dropdown_value])

    return df5.to_dict('records')


@app.callback(Output('active_in_week', 'children'), [Input('module', 'value')])
def update_header(selected_dropdown_value):
    return [html.H4('Total number of students active in week: ' +  str(active_users[selected_dropdown_value]),
                    style={'text-align': 'left'})]


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
    # 'url': '~/Desktop/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)
