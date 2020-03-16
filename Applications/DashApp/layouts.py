import dash_core_components as dcc
import dash_html_components as html
from Applications.DashApp import dataviz

layoutindex = html.Div([
    html.H3('Dash Index'),
    html.Div(id='dash-container',
    children=dataviz.get_datasets())
])

layout1 = html.Div([
    html.H3('App 1'),
    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-1-display-value'),
    dcc.Link('Go to App 2', href='/quadrants/app2')
])

layout2 = html.Div([
    html.H3('App 2'),
    dcc.Dropdown(
        id='app-2-dropdown',
        options=[
            {'label': 'App 2 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-2-display-value'),
    dcc.Link('Go to App 1', href='/quadrants/app1')
])

def layoutquad(ccode, quad):

    countries = {
        'MWI' : 'Malawi',
        'TZA' : 'Tanzania',
        'ZAF' : 'South Africa',
        'ZMB' : 'Zambia'
    }

    country = countries[ccode]

    layout = html.Div([
    html.H3('Data Exploration for {country}, quadrant {quad}'.format(country=country, quad=quad)),
    html.Div(id='dash-container',
    children=dataviz.get_datasets())
    ])

    return layout
