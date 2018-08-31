import dash
import os

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
import plotly.graph_objs as go
from plotly.graph_objs import *

from server import server, Course, Session, Module, ModuleInfo

course = "Robotics: Aerial Robotics"
course_id = Course.query.filter(Course.name == course).first().course_id
sessions = Session.query.filter(Session.course_id == course_id).order_by(Session.start_date)
modules = Module.query.filter(Module.course_id == course_id).order_by(Module.order)


app = dash.Dash(name='story1', sharing=True,
                server=server, url_base_pathname='/story1', csrf_protect=False)

app.layout = html.Div([
    html.H4('Robotics: Aerial Robotics'),

    html.Div(children=[
        html.Label('Session'),
        dcc.Dropdown(
            id='session',
            options=[{'label': '{} - {}'.format(s.start_date.strftime("%Y-%m-%d"), s.end_date.strftime("%Y-%m-%d")), 'value': s.session_id} for s in sessions],
            value='mGhKAXoWEee1jApzGcQi8A',

        ), ],
        style={'marginBottom': 30, 'marginTop': 25, 'marginLeft': 100, 'marginRight': 100}
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
            ],
            value='all'
        ), ],
        style={'marginBottom': 50, 'marginLeft': 100, 'marginRight': 100}
    ),
    html.Div(id='stats'),
    # html.H6('Total number of students enrolled for this time period: 1242.', style={'margin-left': '70'}),
    # html.H6('Total number of active students in this time period: 1646.', style={'margin-left': '70'}),
    # html.H6('Number of students enrolled in previous sessions but active in current session: 1135.',
    #         style={'margin-left': '70'}),
    html.Div(
        children=[
            html.H3(
                '% of ever-active users for whom video was the last video seen before dropping out of or completing the course.',
                style={'text-align': 'center',
                       'padding-bottom': '-1em'}),
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
            'marginLeft': 60,
            'marginRight': 60,
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
                columns=['Course order', 'Assignment', 'Last seen (%)'],
                sortable=True,
                selected_row_indices=[],
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


@app.callback(Output('video_last_seen', 'figure'), [Input('session', 'value'), Input('module', 'value')])
def update_graph(session, module):
    df = pd.read_csv("data_all/{}/{}.csv".format(session, module))

    l = df['last_seen'].tolist()
    s = 1646

    if len(l) < 10:
        count = len(l) - 0.5
    else:
        count = l

    lx = df['video'].tolist()
    ly = [x for x in l]
    # this is probably a bug in plotly - lists are displayed in a reversed order
    lx.reverse()
    ly.reverse()

    return {
        'data': [go.Bar(
            x=lx,
            y=ly
        )],
        'layout': {
            'height': 900,
            'width': 900,
            'yaxis': {
                'tickformat': '%'
            },
            'xaxis': {
                'tickangle': 45,
                'range': [-0.5, count],

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
    df = pd.read_csv("data_all/{}/{}.csv".format(session, module))
    active = 21  # Session.query.filter(Session.session_id==session).first().active_users#active_users[selected_dropdown_value]

    l1 = df['watched'].tolist()
    if len(l1) < 10:
        count = len(l1) - 0.5
    else:
        count = l1

    lx = df['video'].tolist()
    ly = [x for x in l1]
    # probably a bug in plotly
    lx.reverse()
    ly.reverse()

    return {
        'data': [go.Bar(
            x=lx,
            y=ly
        )],
        'layout': {
            'height': 900,
            'width': 900,
            'yaxis': {
                'tickformat': '%'
            },
            'xaxis': {
                'tickangle': 45,
                'range': [-0.5, count],

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


@app.callback(Output('assignment_last_seen', 'figure'), [Input('session', 'value'), Input('module', 'value')])
def update_graph(session, module):
    df = pd.read_csv("data_all/{}/{}_assignments.csv".format(session, module))

    l3 = df['last_seen'].tolist()

    return {
        'data': [go.Bar(
            x=df['name'].tolist(),
            y=[x for x in l3]
        )],
        'layout': {
            'yaxis': {
                'tickformat': '%'
            },
            'xaxis': {
                'type': 'category'
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


@app.callback(Output('assignments_tables', 'rows'), [Input('module', 'value'), Input('session', 'value')])
def update_graph(module, session):
    if module != 'all':
        m = ModuleInfo.query.filter(ModuleInfo.session_id == session).filter(ModuleInfo.module_id == module).first()
        df = pd.read_csv("data_all/{}/{}_assignments_table.csv".format(session, module))

    else:
        df = pd.read_csv("data_all/{}/assignments_table.csv".format(session))

    return df.to_dict('records')


@app.callback(Output('active_in_week', 'children'), [Input('module', 'value'), Input('session', 'value')])
def update_header(module, session):
    if module != 'all':
        m = ModuleInfo.query.filter(ModuleInfo.session_id == session).filter(ModuleInfo.module_id == module).first()

        return [html.H4('Total number of students active in week: ' + str(m.active_users),
                        style={'text-align': 'left'})]
    else:
        s = Session.query.filter(Session.session_id == session).first()
        active = s.active_users
        return [html.H4('Total number of students active in time period: ' + str(active),
                        style={'text-align': 'left'})]


@app.callback(Output('stats', 'children'), [Input('session', 'value')])
def update_header(session):
    s = Session.query.filter(Session.session_id == session).first()
    print(type(s.start_date))
    return [
        html.H6('Total number of students enrolled for this time period: ' + str(s.users_enrolled), style={'margin-left': '70'}),
        html.H6('Total number of active students in this time period: ' + str(s.active_users), style={'margin-left': '70'}),
        html.H6('Number of students enrolled in previous sessions but active in current session: ' + str(s.active_users - s.active_users_enrolled),
             style={'margin-left': '70'}),]


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
