import dash_html_components as html
import dash_core_components as dcc
from Applications.DashApp import dataviz
from Applications.DashApp.axisdicts import *
import re

def layoutquad(ccode, quad):

    country = countrydict[ccode]

    layout = html.Div([
        html.H3(children='Data Exploration for {country} with {quad}'.format(country=country, quad=re.sub(',',' and', quaddict[ccode][quad])),
                style={'textAlign': 'center', "margin-bottom":"15px"}),
        html.Div([
            dcc.Dropdown(
                id='crop',
                options=[{'label': v, 'value': k} for k,v in cropdict.items()],
                value=0
            )
        ], style={'width': '20%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='field',
                options=[{'label': v, 'value': k} for k,v in fielddict.items()],
                value='yield'
            )
        ], style={'width': '20%', 'display': 'inline-block'}),
        dcc.Loading(id='loading-1',
                    children=[dcc.Graph(id='cropgraph')],
                    type='circle',
                    )
    ])

    return layout

def layoutquadcompar(ccode):

    country = countrydict[ccode]

    layout = html.Div([
        html.H3(children='Data Exploration for {country} with cross-quadrant comparisons'.format(country=country),
                style={'textAlign': 'center', "margin-bottom":"15px"}),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='quad1',
                    options=[{'label': v, 'value': k} for k,v in quaddict[ccode].items()],
                    value="00"
                    )
                ], style={'width': '50%'}
            ),
            html.Div([
                dcc.Dropdown(
                    id='crop1',
                    options=[{'label': v, 'value': k} for k,v in cropdict.items()],
                    value=0
                    )
                ], style={'width': '25%', 'display': 'inline-block'}
            ),
            html.Div([
                dcc.Dropdown(
                    id='field1',
                    options=[{'label': v, 'value': k} for k,v in fielddict.items()],
                    value='yield'
                    )
                ], style={'width': '25%', 'display': 'inline-block'}
            ),
            html.Div([
                dcc.Loading(
                    id='loading-1',
                    children=[dcc.Graph(id='compgraph1')],
                    type='graph',
                    )
                ], style={"border":"thin solid #999999", "height":"550px"}
            )
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='quad2',
                    options=[{'label': v, 'value': k} for k,v in quaddict[ccode].items()],
                    value="11"
                    )
                ], style={'width': '50%'}
            ),
            html.Div([
                dcc.Dropdown(
                    id='crop2',
                    options=[{'label': v, 'value': k} for k,v in cropdict.items()],
                    value=0
                    )
                ], style={'width': '25%', 'display': 'inline-block'}
            ),
            html.Div([
                dcc.Dropdown(
                    id='field2',
                    options=[{'label': v, 'value': k} for k,v in fielddict.items()],
                    value='yield'
                    )
                ], style={'width': '25%', 'display': 'inline-block'}
            ),
            html.Div([
                dcc.Loading(
                    id='loading-2',
                    children=[dcc.Graph(id='compgraph2')],
                    type='graph',
                    )
                ], style={"border":"thin solid #999999", "height":"550px"}
            )
        ], style={'width': '50%', 'display': 'inline-block'})
    ], style={'width': '95%'})

    return layout

def layoutfullcompar():


    layout = html.Div([
        html.H3(children='Data Exploration for cross-country comparisons',
                style={'textAlign': 'center', "margin-bottom":"15px"}),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='ccode1',
                    options=[{'label': v, 'value': k} for k,v in countrydict.items()],
                    value="MWI"
                    )
                ], style={'width': '50%'}
            ),
            html.Div([
                dcc.Dropdown(id='quad1-dropdown')
                ], style={'width': '50%'}
            ),
            html.Div([
                dcc.Dropdown(
                    id='crop1',
                    options=[{'label': v, 'value': k} for k,v in cropdict.items()],
                    value=0
                    )
                ], style={'width': '25%', 'display': 'inline-block'}
            ),
            html.Div([
                dcc.Dropdown(
                    id='field1',
                    options=[{'label': v, 'value': k} for k,v in fielddict.items()],
                    value='yield'
                    )
                ], style={'width': '25%', 'display': 'inline-block'}
            ),
            html.Div([
                dcc.Loading(
                    id='loading-1',
                    children=[dcc.Graph(id='fullcompgraph1')],
                    type='cube',
                    )
                ], style={"border":"thin solid #999999", "height":"550px"}
            )
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='ccode2',
                    options=[{'label': v, 'value': k} for k,v in countrydict.items()],
                    value="ZAF"
                    )
                ], style={'width': '50%'}
            ),
            html.Div([
                dcc.Dropdown(id='quad2-dropdown')
                ], style={'width': '50%'}
            ),
            html.Div([
                dcc.Dropdown(
                    id='crop2',
                    options=[{'label': v, 'value': k} for k,v in cropdict.items()],
                    value=0
                    )
                ], style={'width': '25%', 'display': 'inline-block'}
            ),
            html.Div([
                dcc.Dropdown(
                    id='field2',
                    options=[{'label': v, 'value': k} for k,v in fielddict.items()],
                    value='yield'
                    )
                ], style={'width': '25%', 'display': 'inline-block'}
            ),
            html.Div([
                dcc.Loading(
                    id='loading-2',
                    children=[dcc.Graph(id='fullcompgraph2')],
                    type='cube',
                    )
                ], style={"border":"thin solid #999999", "height":"550px"}
            )
        ], style={'width': '50%', 'display': 'inline-block'})
    ], style={'width': '95%', 'margin': '0 auto 0 auto'})

    return layout
