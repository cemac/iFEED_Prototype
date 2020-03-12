from dash.dependencies import Input, Output
import dash_html_components as html
from flask import abort

from Applications.app import app


@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

@app.callback(
    Output('app-2-display-value', 'children'),
    [Input('app-2-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)


#@app.callback(Output('page-content', 'children'),
#             [Input('url', 'pathname')])
#def display_page(pathname):
#
#    ccodelst = ['MWI','TZA','ZAF','ZMB']
#    quadlst = ['00','01','10','11']
#
#    err=False
#
#    if not pathname[:11] == "/quadrants/":
#        err=True
#    elif not pathname[11:14] in ccodelst:
#        err=True
#    elif not pathname[14:] in quadlst:
#        err=True
#
#    if err:
#        return abort(404)
#    else:
#        return html.Div([
#            html.H3('You are on page {}'.format(pathname))
#    ])
