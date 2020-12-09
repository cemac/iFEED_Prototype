from dash.dependencies import Input, Output
from Applications.DashApp import dataviz
from Applications.DashApp.axisdicts import quaddict
from Applications.app import app


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

@app.callback(
    Output('compgraph1', 'figure'),
    [Input('crop1', 'value'),
     Input('field1', 'value'),
     Input('quad1', 'value'),
     Input('intermediate-value', 'children')])
def update_quad1_graph(crop1, field1, quad1, loclst):

    ccode=loclst[0]

    df = dataviz.get_cubedata(ccode, quad1, field1)
    fig = dataviz.compgraph(ccode, quad1, crop1, df, field1)

    return fig

@app.callback(
    Output('compgraph2', 'figure'),
    [Input('crop2', 'value'),
     Input('field2', 'value'),
     Input('quad2', 'value'),
     Input('intermediate-value', 'children')])
def update_quad2_graph(crop2, field2, quad2, loclst):

    ccode=loclst[0]

    df = dataviz.get_cubedata(ccode, quad2, field2)
    fig = dataviz.compgraph(ccode, quad2, crop2, df, field2)

    return fig

@app.callback(
    Output('fullcompgraph1', 'figure'),
    [Input('ccode1', 'value'),
     Input('crop1', 'value'),
     Input('field1', 'value'),
     Input('quad1-dropdown', 'value'),
     Input('intermediate-value', 'children')])
def update_count1_graph(ccode1, crop1, field1, quad1, loclst):

    if quad1 == None:
        quad1 == '00'

    df = dataviz.get_cubedata(ccode1, quad1, field1)
    fig = dataviz.compgraph(ccode1, quad1, crop1, df, field1)

    return fig

@app.callback(
    Output('fullcompgraph2', 'figure'),
    [Input('ccode2', 'value'),
     Input('crop2', 'value'),
     Input('field2', 'value'),
     Input('quad2-dropdown', 'value'),
     Input('intermediate-value', 'children')])
def update_count2_graph(ccode2, crop2, field2, quad2, loclst):

    if quad2 == None:
        quad2 == '00'

    df = dataviz.get_cubedata(ccode2, quad2, field2)
    fig = dataviz.compgraph(ccode2, quad2, crop2, df, field2)

    return fig

@app.callback(
    Output('quad1-dropdown', 'options'),
    [Input('ccode1', 'value')])
def set_quad2_options(ccode1):
    return [{'label': v, 'value': k} for k,v in quaddict[ccode1].items()]

@app.callback(
    Output('quad1-dropdown', 'value'),
    [Input('quad1-dropdown', 'options')])
def set_quad2_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output('quad2-dropdown', 'options'),
    [Input('ccode2', 'value')])
def set_quad2_options(ccode2):
    return [{'label': v, 'value': k} for k,v in quaddict[ccode2].items()]

@app.callback(
    Output('quad2-dropdown', 'value'),
    [Input('quad2-dropdown', 'options')])
def set_quad2_value(available_options):
    return available_options[0]['value']

#@app.callback(
#    Output('loading-2','style'),
#    [Input('fullcompgraph2','figure')]
#)
#def f(fig):
#    if not fig is None:
#        return dict(border="thin solid #999999")
#    else:
#        return dict()
