import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import abort

from Applications.app import app
from Applications.DashApp.layouts import layoutindex, layout1, layout2
import Applications.DashApp.callbacks
from Applications.DashApp import dataviz

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/quadrants/index':
         return layoutindex
    elif pathname == '/quadrants/app1':
         return layout1
    elif pathname == '/quadrants/app2':
         return layout2
    else:
        return abort(404)
