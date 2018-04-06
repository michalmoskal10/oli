import dash
import os

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
import plotly.graph_objs as go
from plotly.graph_objs import *



from server import server

with open('.pass') as f:
    VALID_USERNAME_PASSWORD_PAIRS = [x.strip().split(':') for x in f.readlines()]

first_attempts = {
    'Quiz 1.1': 'data/story2/assignment_1_1/first_attempt.csv',
    'Quiz 1.2': 'data/story2/assignment_1_2/first_attempt.csv',
    'Quiz 2.1': 'data/story2/assignment_2_1/first_attempt.csv',
    'Quiz 3': 'data/story2/week4.csv',
    'Quiz 4': 'data/story2/week4.csv',
    'all': 'data/story2/all.csv'
}

second_attempts = {
    'Quiz 1.1': 'data/story2/assignment_1_1/second_attempt.csv',
    'Quiz 1.2': 'data/story2/assignment_1_2/second_attempt.csv',
    'Quiz 2.1': 'data/story2/assignment_2_1/second_attempt.csv',
    'Quiz 3': 'data/story2/week4.csv',
    'Quiz 4': 'data/story2/week4.csv',
    'all': 'data/story2/all.csv'
}

attempts_to_correct = {
    'Quiz 1.1': 'data/story2/assignment_1_1/attempts_to_correct.csv',
    'Quiz 1.2': 'data/story2/assignment_1_2/attempts_to_correct.csv',
    'Quiz 2.1': 'data/story2/assignment_2_1/attempts_to_correct.csv',
    'Quiz 3': 'data/story2/week4.csv',
    'Quiz 4': 'data/story2/week4.csv',
    'all': 'data/story2/all.csv'
}

never_correct = {
    'Quiz 1.1': 'data/story2/assignment_1_1/never_correct.csv',
    'Quiz 1.2': 'data/story2/assignment_1_2/never_correct.csv',
    'Quiz 2.1': 'data/story2/assignment_2_1/never_correct.csv',
    'Quiz 3': 'data/story2/week4.csv',
    'Quiz 4': 'data/story2/week4.csv',
    'all': 'data/story2/all.csv'
}




app = dash.Dash(name='story2', sharing=True,
                server=server, url_base_pathname='/story2', csrf_protect=False)

# auth = dash_auth.BasicAuth(
#     app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )

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
        html.Label('Assignment'),
        dcc.Dropdown(
            id='assignment',
            options=[
                {'label': 'Quiz 1.1', 'value': 'Quiz 1.1'},
                {'label': 'Quiz 1.2', 'value': 'Quiz 1.2'},
                {'label': 'Quiz 2.1', 'value': 'Quiz 2.1'},
                {'label': 'Quiz 3', 'value': 'Week4'},
                {'label': 'Quiz 4', 'value': 'all'},
                {'label': 'All', 'value': 'all'},

            ],
            value='Quiz 1.1'
        ), ],
        style={'marginBottom': 50, 'marginLeft': 100, 'marginRight': 100}
    ),

      html.Div(
        children=[
            html.H2('First attempt error rate.',
                    style={'text-align':'center',
                           'padding-bottom':'-1em'}),
            dcc.Graph(id='first_attempt'),

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
            html.H2('Second attempt error rate',
                    style={'text-align':'center',
                           'padding-bottom':'-1em'}),
            dcc.Graph(id='second_attempt'),
        ],
        style={
            'marginLeft': 60,
            'marginRight': 60,
            'marginBottom': 90,
            'marginTop': 0
        }
    ),
    html.Div(
        children=[
            html.H2('Attempts to correct (avarage).',
                    style={'text-align': 'center',
                           'padding-bottom': '-1em'}),
            dcc.Graph(id='attempts_to_correct'),
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
            html.H2('Percent who attempt, but never correct.',
                    style={'text-align': 'center',
                           'padding-bottom': '-1em'}),
            dcc.Graph(id='never_correct'),
        ],
        style={
            'marginLeft': 60,
            'marginRight': 60,
            'marginBottom': 50,
            'marginTop': 0
        }
    ),

],
    className="container"
)

@app.callback(Output('first_attempt', 'figure'), [Input('assignment', 'value')])
def update_graph(selected_dropdown_value):
    #df = web.DataReader(
    #    selected_dropdown_value, data_source='google',
    #    start=dt(2017, 1, 1), end=dt.now())
    df = pd.read_csv(first_attempts[selected_dropdown_value])

    df['error'] = (df['all'] - df['correct']) / df['all']
    df.sort_values(by=['error'], ascending=False, inplace=True)

    l = len(df.index)
    if l < 10:
        range = l - 0.5
    else:
        range = 9.5
    return {
        # 'data': [{
        #     'x': df.index,
        #     'y': df.values,
        #     'type': 'bar'
        # }]
        'data': [go.Bar(
            x=df['name'].tolist(),
            y=df['error'].tolist()
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

@app.callback(Output('second_attempt', 'figure'), [Input('assignment', 'value')])
def update_graph(selected_dropdown_value):
    #df = web.DataReader(
    #    selected_dropdown_value, data_source='google',
    #    start=dt(2017, 1, 1), end=dt.now())
    df = pd.read_csv(second_attempts[selected_dropdown_value])

    df['error'] = (df['all'] - df['correct']) / df['all']
    df.sort_values(by=['error'], ascending=False, inplace=True)

    l = len(df.index)
    if l < 10:
        range = l - 0.5
    else:
        range = 9.5
    return {
        # 'data': [{
        #     'x': df.index,
        #     'y': df.values,
        #     'type': 'bar'
        # }]
        'data': [go.Bar(
            x=df['name'].tolist(),
            y=df['error'].tolist()
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


@app.callback(Output('attempts_to_correct', 'figure'), [Input('assignment', 'value')])
def update_graph(selected_dropdown_value):
    #df = web.DataReader(
    #    selected_dropdown_value, data_source='google',
    #    start=dt(2017, 1, 1), end=dt.now())
    df = pd.read_csv(attempts_to_correct[selected_dropdown_value])

    df.sort_values(by='avg', ascending=False, inplace=True)
    l = len(df.index)
    if l < 10:
        range = l - 0.5
    else:
        range = 9.5
    return {
        # 'data': [{
        #     'x': df.index,
        #     'y': df.values,
        #     'type': 'bar'
        # }]
        'data': [go.Bar(
            x=df['name'].tolist(),
            y=df['avg'].tolist()
        )],
        'layout':{
            'height': 900,
            'width': 900,

            'xaxis': {
                'tickangle': 45,
                'range': [-0.5, range],

            },

            'margin': Margin(b=350)
        }
    }


@app.callback(Output('never_correct', 'figure'), [Input('assignment', 'value')])
def update_graph(selected_dropdown_value):
    #df = web.DataReader(
    #    selected_dropdown_value, data_source='google',
    #    start=dt(2017, 1, 1), end=dt.now())
    df = pd.read_csv(never_correct[selected_dropdown_value])

    df['never_correct_percent'] = df['never_correct'] / df['all']
    df.sort_values(by='never_correct_percent', ascending=False, inplace=True)
    l = len(df.index)

    if l < 10:
        range = l - 0.5
    else:
        range = 9.5
    return {
        # 'data': [{
        #     'x': df.index,
        #     'y': df.values,
        #     'type': 'bar'
        # }]
        'data': [go.Bar(
            x=df['name'].tolist(),
            y=df['never_correct_percent'].tolist()
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

            'margin': Margin(b=350)
        }
    }

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
    # 'url': '~/Desktop/bWLwgP.css'
})

# if __name__ == '__main__':
#     app.run_server(debug=True)
