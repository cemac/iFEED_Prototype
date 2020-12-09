import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from Applications.app import app
from Applications.DashApp.layouts import layoutquad, layoutquadcompar, layoutfullcompar
from Applications.DashApp.errors import layout404

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='intermediate-value', style={'display': 'none'}),
    html.Div(id='page-content')
])

@app.callback([Output('page-content', 'children'),
               Output('intermediate-value', 'children')],
             [Input('url', 'pathname')])
def display_page(pathname):

    ccodelst = ['MWI','TZA','ZAF','ZMB','ALL']
    quadlst = ['00','01','10','11','comp']

    err=False

    if not pathname[:18] == "/data_exploration/":
        err=True
    elif not pathname[18:21] in ccodelst:
        err=True
    elif not pathname[21:] in quadlst:
        err=True

    if err:
        return layout404
    elif pathname[18:] == 'ALLcomp':
        return layoutfullcompar(), [pathname[18:21],pathname[21:]]
    elif (pathname[21:] == 'comp' and pathname[18:21] != 'ALL'):
        return layoutquadcompar(pathname[18:21]), [pathname[18:21],pathname[21:]]
    else:
        return layoutquad(pathname[18:21],pathname[21:]), [pathname[18:21],pathname[21:]]
