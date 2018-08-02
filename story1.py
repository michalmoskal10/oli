import dash
import os

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
import plotly.graph_objs as go
from plotly.graph_objs import *


from server import server, Course, Session, Module

course = "Robotics: Aerial Robotics"
course_id = Course.query.filter(Course.name==course).first().course_id
sessions = Session.query.filter(Session.course_id==course_id).order_by(Session.start_date)
modules = Module.query.filter(Module.course_id==course_id)

files_videos = {
    'Week1': 'data/story1/week1.csv',
    'Week2': 'data/story1/week2.csv',
    'Week3': 'data/story1/week3.csv',
    'Week4': 'data/story1/week4.csv',
    'all': 'data/story1/all.csv'
}

files_assignments = {
    'Week1': 'data/story1/week1_assignments.csv',
    'Week2': 'data/story1/week2_assignments.csv',
    'Week3': 'data/story1/week3_assignments.csv',
    'Week4': 'data/story1/week4_assignments.csv',
    'all': 'data/story1/all_ass.csv'
}

files_assignments_table = {
    'Week1': 'data/story1/week1_assignments_table.csv',
    'Week2': 'data/story1/week2_assignments_table.csv',
    'Week3': 'data/story1/week3_assignments_table.csv',
    'Week4': 'data/story1/week4_assignments_table.csv',
    'all': 'data/story1/assignments_tables.csv'
}

active_users = {
    'Week1':1338,
    'Week2':648,
    'Week3':351,
    'Week4':303,
    'all': 1646
}




app = dash.Dash(name='story1', sharing=True,
                server=server, url_base_pathname='/story1', csrf_protect=False)

app.layout = html.Div([
    html.H4('Robotics: Aerial Robotics'),


    html.Div(children=[
            html.Label('Session'),
            dcc.Dropdown(
                id='session',
                options=[{'label': '{} - {}'.format(s.start_date, s.end_date), 'value': s.session_id} for s in sessions]
            ),],
        style={'marginBottom': 30, 'marginTop': 25, 'marginLeft': 100, 'marginRight':100}
    ),

    html.Div(children=[
        html.Label('Module'),
        dcc.Dropdown(
            id='module',
            options=
            [
                {'label': '{}. {}'.format(m.order + 1, m.name), 'value': m.module_id} for m in modules
            ] +
            [
                {'label': 'All modules', 'value': 'all'},
            ]
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
                id='assignments_tables',
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
def update_graph(session, module):
    df = pd.read_csv("data/{}/{}.csv".format(session, module))

    l = df['last_seen'].tolist()
    s = 1646

    if len(l) < 10:
        range = len(l) - 0.5
    else:
        range = l
    return {
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

@app.callback(Output('watched', 'figure'), [Input('session', 'value'), Input('module', 'value')])
def update_graph(session, module):
    df = pd.read_csv("data/{}/{}.csv".format(session, module))
    active = 21#Session.query.filter(Session.session_id==session).first().active_users#active_users[selected_dropdown_value]

    l1 = df['watched'].tolist()
    if len(l1) < 10:
        range = len(l1) - 0.5
    else:
        range = l1
    return {
        'data': [go.Bar(
            x=df['video'].tolist(),
            y=[x/active for x in l1]
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
    df3 = pd.read_csv(files_assignments[selected_dropdown_value])


    l3 = df3['last_seen'].tolist()
    s3 = 896

    return {
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


@app.callback(Output('assignments_tables', 'rows'), [Input('module', 'value')])
def update_graph(selected_dropdown_value):
    df5 = pd.read_csv(files_assignments_table[selected_dropdown_value])

    return df5.to_dict('records')


@app.callback(Output('active_in_week', 'children'), [Input('module', 'value')])
def update_header(selected_dropdown_value):
    if selected_dropdown_value != 'all':
        return [html.H4('Total number of students active in week: ' +  str(active_users[selected_dropdown_value]),
                    style={'text-align': 'left'})]
    else:
        return [html.H4('Total number of students active in time period: ' +  str(active_users[selected_dropdown_value]),
                    style={'text-align': 'left'})]

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
