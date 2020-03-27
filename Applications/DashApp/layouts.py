import dash_html_components as html
import dash_core_components as dcc
from Applications.DashApp import dataviz
from Applications.DashApp.axisdicts import *

def layoutquad(ccode, quad):

    country = countrydict[ccode]

    layout = html.Div([
        html.H3('Data Exploration for {country}, quadrant {quad}'.format(country=country, quad=quad)),
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
