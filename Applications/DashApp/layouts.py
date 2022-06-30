import dash_html_components as html
import dash_core_components as dcc
from Applications.DashApp import dataviz
from Applications.DashApp.axisdicts import countrydict, cropdict, fielddict, quaddict
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
                value=2
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
    ], style={'width': '75%', 'margin':'auto'})

    return layout

def layoutquadcustom(ccode, clim):

    country = countrydict[ccode]

    layout = html.Div([
        html.H3(children='Data Exploration for {country} with {clim} Climate Risk'.format(country=country, clim=clim),
                style={'textAlign': 'center', "margin-bottom":"15px"}),
        html.Br(),
        html.H6(children='Here you can directly view how parameters such as yield and growing season duration vary with irrigation and yield gap parameter (YGP) for futures with {} Climate Risk.  Zero irrigation indicates crops are purely rainfed. Irrigation of 1 refers to fully irrigated simulations (i.e. no water stress), with intermediate values corresponding to intermediate irrigation scenarios. A yield gap parameter of 1 indicates climatic potential yields. Default yield gap parameter values - representative of observed yield values for the year 2000 - are given for each crop.'.format(clim), style={'textAlign': 'center', "margin-bottom":"15px"}),
        html.Br(),
        html.Div([
            html.Div([
                html.H6(children='Crop',style={'textAlign': 'center',}),
                dcc.Dropdown(
                    id='crop',
                    options=[{'label': v, 'value': k} for k,v in cropdict.items()],
                    value=2
                )
            ], style={'width': '25%', 'display': 'inline-block', 'margin-right':'4%'}),
            html.Div([
                html.H6(children='Parameter',style={'textAlign': 'center',}),
                dcc.Dropdown(
                    id='field',
                    options=[{'label': v, 'value': k} for k,v in fielddict.items()],
                    value='yield'
                )
            ], style={'width': '25%', 'display': 'inline-block', 'margin-left':'4%'})
        ], style={ 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
        html.Div([
            html.Div([
                html.H6(children='Irrigation',style={'textAlign': 'center',}),
                dcc.Slider(
                    min = 0,
                    max = 1,
                    step = 0.1,
                    value=0,
                    marks={"{:.1f}".format(i * 0.1):"{:.1f}".format(i * 0.1) for i in range(0,11,1)},
                    id='irr'
                    )
                ], style={'width': '33%', 'display': 'inline-block', 'margin-bottom': '20px'}
            ),
            html.Div([
                html.H6(children='YGP',style={'textAlign': 'center',}),
                dcc.Slider(
                    min = 0.1,
                    max = 1,
                    step = 0.1,
                    value=0.1,
                    marks={"{:.1f}".format((i+1) * 0.1):"{:.1f}".format((i+1) * 0.1) for i in range(0,10,1)},
                    id='ygp',
                    )
                ], style={'width': '33%', 'display': 'inline-block', 'margin-bottom': '20px'}
            )
        ], style={ 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
        dcc.Loading(id='loading-1',
                    children=[dcc.Graph(id='cropgraph2')],
                    type='circle',
                    )
    ], style={'width': '75%', 'margin':'auto'})

    return layout

def layoutquadcompar(ccode):

    country = countrydict[ccode]

    layout = html.Div([
        html.H3(children='Data Exploration for {country} with Comparisons Across Climate Scenarios'.format(country=country),
                style={'textAlign': 'center', "margin-bottom":"15px"}),
        html.Br(),
        html.H6(children='Here you can directly compare how parameters such as yield and growing duration vary with irrigation and yield gap parameter for both Low Climate Risk and High Climate Risk scenarios.  Zero irrigation here indicates crops are purely rain-fed. Default yield gap parameter values are given for each crop.', style={'textAlign': 'center', "margin-bottom":"15px"}),
        html.Br(),
        html.Div([
            html.Div([
                html.H5(children='Low Climate Risk', style={'textAlign':'center'})
            ]),
            html.Div([
                html.Div([
                    html.H6(children='Crop',style={'textAlign': 'center',}),
                    dcc.Dropdown(
                        id='crop1',
                        options=[{'label': v, 'value': k} for k,v in cropdict.items()],
                        value=2
                        )
                    ], style={'width': '33%', 'display': 'inline-block', 'margin-bottom': '20px'}
                ),
                html.Div([
                    html.H6(children='Parameter',style={'textAlign': 'center',}),
                    dcc.Dropdown(
                        id='field1',
                        options=[{'label': v, 'value': k} for k,v in fielddict.items()],
                        value='yield'
                        )
                    ], style={'width': '33%', 'display': 'inline-block', 'margin-bottom': '20px'}
                ),
            ], style={ 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
            html.Div([
                html.Div([
                    html.H6(children='Irrigation',style={'textAlign': 'center',}),
                    dcc.Slider(
                        min = 0,
                        max = 1,
                        step = 0.1,
                        value=0,
                        marks={"{:.1f}".format(i * 0.1):"{:.1f}".format(i * 0.1) for i in range(0,10,2)},
                        id='irr1'
                        )
                    ], style={'width': '33%', 'display': 'inline-block', 'margin-bottom': '20px'}
                ),
                html.Div([
                    html.H6(children='YGP',style={'textAlign': 'center',}),
                    dcc.Slider(
                        min = 0.1,
                        max = 1,
                        step = 0.1,
                        value=0.1,
                        marks={"{:.1f}".format(i * 0.1):"{:.1f}".format(i * 0.1) for i in range(0,10,2)},
                        id='ygp1',
                        )
                    ], style={'width': '33%', 'display': 'inline-block', 'margin-bottom': '20px'}
                )
            ], style={ 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
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
                html.H5(children='High Climate Risk', style={'textAlign':'center'})
            ]),
            html.Div([
                html.Div([
                    html.H6(children='Crop',style={'textAlign': 'center',}),
                    dcc.Dropdown(
                        id='crop2',
                        options=[{'label': v, 'value': k} for k,v in cropdict.items()],
                        value=2
                        )
                    ], style={'width': '33%', 'display': 'inline-block', 'margin-bottom': '20px'}
                ),
                html.Div([
                    html.H6(children='Parameter',style={'textAlign': 'center',}),
                    dcc.Dropdown(
                        id='field2',
                        options=[{'label': v, 'value': k} for k,v in fielddict.items()],
                        value='yield'
                        )
                    ], style={'width': '33%', 'display': 'inline-block', 'margin-bottom': '20px'}
                ),
            ], style={ 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
            html.Div([
                html.Div([
                    html.H6(children='Irrigation',style={'textAlign': 'center',}),
                    dcc.Slider(
                        min = 0,
                        max = 1,
                        step = 0.1,
                        value=0,
                        marks={"{:.1f}".format(i * 0.1):"{:.1f}".format(i * 0.1) for i in range(0,10,2)},
                        id='irr2'
                        )
                    ], style={'width': '33%', 'display': 'inline-block', 'margin-bottom': '20px'}
                ),
                html.Div([
                    html.H6(children='YGP',style={'textAlign': 'center',}),
                    dcc.Slider(
                        min = 0.1,
                        max = 1,
                        step = 0.1,
                        value=0.1,
                        marks={"{:.1f}".format(i * 0.1):"{:.1f}".format(i * 0.1) for i in range(0,10,2)},
                        id='ygp2',
                        )
                    ], style={'width': '33%', 'display': 'inline-block', 'margin-bottom': '20px'}
                )
            ], style={ 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
            html.Div([
                dcc.Loading(
                    id='loading-2',
                    children=[dcc.Graph(id='compgraph2')],
                    type='graph',
                    )
                ], style={"border":"thin solid #999999", "height":"550px"}
            )
        ], style={'width': '50%', 'display': 'inline-block'})
    ], style={'width': '75%', 'margin':'auto'})

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
    ], style={'width': '75%', 'margin': '0 auto 0 auto'})

    return layout
