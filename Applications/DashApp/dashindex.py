import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import abort

from Applications.app import app
from Applications.DashApp.layouts import *
from Applications.DashApp.errors import *
import Applications.DashApp.callbacks
from Applications.DashApp import dataviz

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='intermediate-value', style={'display': 'none'}),
    html.Div(id='page-content')
])

@app.callback([Output('page-content', 'children'),
               Output('intermediate-value', 'children')],
             [Input('url', 'pathname')])
def display_page(pathname):

    ccodelst = ['MWI','TZA','ZAF','ZMB']
    quadlst = ['00','01','10','11']

    err=False

    if not pathname[:11] == "/quadrants/":
        err=True
    elif not pathname[11:14] in ccodelst:
        err=True
    elif not pathname[14:] in quadlst:
        err=True

    if err:
        return layout404
    else:
        return layoutquad(pathname[11:14],pathname[14:]), [pathname[11:14],pathname[14:]]