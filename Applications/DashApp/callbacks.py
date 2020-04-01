from dash.dependencies import Input, Output
from Applications.DashApp import dataviz
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


@app.callback(
    Output('cropgraph', 'figure'),
    [Input('crop', 'value'),
     Input('field', 'value'),
     Input('intermediate-value', 'children')])
def update_graph(crop, field, loclst):

    ccode=loclst[0]
    quad = loclst[1]

    df = dataviz.get_cubedata(ccode, quad, field)
    fig = dataviz.cropgraph(ccode, quad, crop, df, field)

    return fig
