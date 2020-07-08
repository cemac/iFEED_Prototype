from pathlib import Path
import dash_table
import pandas as pd
import iris
import re
import iris.pandas
import plotly.graph_objs as go
import iris.analysis.cartography
from plotly.subplots import make_subplots
from Applications.DashApp.axisdicts import *

def get_cubedata(ccode, quad, field):

    if ccode == None:
        ccode = "MWI"

    if field == None:
        field = 'yield'

    if quad==None:
        quad='00'

    if (ccode == 'MWI' or ccode == 'TZA'):
        fname = 'data/malawi.nc'
    else:
        fname = 'data/safrica.nc'

    fieldcon = iris.Constraint(field)

    if ccode == 'MWI' or ccode == 'ZMB':
        if quad == '01':
            quadselect = iris.Constraint(rcp=2, irr_lev=0, prod_lev=0.5)
        elif quad == '10':
            quadselect = iris.Constraint(rcp=0, irr_lev=2, prod_lev=0.5)
        elif quad == '11':
            quadselect = iris.Constraint(rcp=2, irr_lev=2, prod_lev=0.5)
        else:
            quadselect = iris.Constraint(rcp=0, irr_lev=0, prod_lev=0.5)
    else:
        if quad == '01':
            quadselect = iris.Constraint(rcp=2, irr_lev=0.5, prod_lev=0.1)
        elif quad == '10':
            quadselect = iris.Constraint(rcp=0, irr_lev=0.5, prod_lev=1.0)
        elif quad == '11':
            quadselect = iris.Constraint(rcp=2, irr_lev=0.5, prod_lev=1.0)
        else:
            quadselect = iris.Constraint(rcp=0, irr_lev=0.5, prod_lev=0.1)

    cube = iris.load(fname).extract(fieldcon)

    for coord in cube[0].coords():
        coord.rename(coord.var_name)

    quadcube = cube[0].extract(quadselect)

    quadcube.coord('lat').guess_bounds()
    quadcube.coord('lon').guess_bounds()

    countrycube = quadcube.collapsed(['lat', 'lon'], iris.analysis.MEAN)

    dflst = []

    for crop in countrycube.coord('crop').points:
        df = iris.pandas.as_data_frame(countrycube.extract(iris.Constraint(crop=crop)))

        linedf = df.quantile(q=[0.0, 0.25, 0.5, 0.75, 1.0], axis=1).T

        boxdf = df.iloc[[0,-1],:].T

        dflst.append([linedf, boxdf])

    return dflst


def cropgraph(ccode, quad, crop, croplst, field):

    if quad==None:
        quad='00'

    df = croplst[crop][0]
    dfbox = croplst[crop][1]

    x = list(df.index)
    x_rev = x[::-1]

    q1 = list(df[0.25])
    q1_rev = q1[::-1]

    q3 = list(df[0.75])

    fig = make_subplots(
        rows=1,
        cols=2,
        column_widths=[0.6, 0.4],
        specs=[[{"type": "scatter"}, {"type": "box"}]]
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df[0.00],
            line_color='firebrick',
            line_width=1,
            line_dash='dot',
            name='Minima',
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=x+x_rev,
            y=q3+q1_rev,
            fill='toself',
            fillcolor='rgba(231,107,243,0.2)',
            line_color='firebrick',
            line_width=0.5,
            name='IQR',
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df[0.25],
            line_color='firebrick',
            line_width=0,
            showlegend=False,
            name='Lower Quartile',
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df[0.50],
            line_color='firebrick',
            line_width=2,
            name='Median',
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df[0.75],
            line_color='firebrick',
            line_width=0,
            showlegend=False,
            name='Upper Quartile',
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df[1.00],
            line_color='firebrick',
            line_width=1,
            line_dash='dot',
            name='Maxima',
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Box(
            y=dfbox.iloc[:,0],
            name=list(dfbox.columns)[0],
            boxpoints=False,
            line=dict(
                color='firebrick'),
            showlegend=False,
            boxmean='sd'
        ),
        row=1,
        col=2
    )

    fig.add_trace(
        go.Box(
            y=dfbox.iloc[:,1],
            name=list(dfbox.columns)[1],
            boxpoints=False,
            line=dict(
                color='firebrick'),
            showlegend=False,
            boxmean='sd',
            yaxis='y'
        ),
        row=1,
        col=2
    )

    fig.update_xaxes(title_text="Year", row=1, col=2)
    fig.update_yaxes(title_text=fielddict[field], hoverformat='.4g', row=1, col=2)

    fig.update_layout(title=cropdict[crop] + ' in ' + countrydict[ccode] + ' for quadrant ' + quad,
                      xaxis_title='Year',
                      yaxis=dict(title=fielddict[field], hoverformat='.4g'),
                      hovermode='x',
                      height=550,
                      margin=dict(
                        l=50,
                        r=50,
                        b=100,
                        t=100,
                        pad=4
                      ),
                      paper_bgcolor="White",)

    return fig


def compgraph(ccode, quad, crop, croplst, field):

    if quad==None:
        quad='00'

    df = croplst[crop][0]
    dfbox = croplst[crop][1]

    x = list(df.index)
    x_rev = x[::-1]

    q1 = list(df[0.25])
    q1_rev = q1[::-1]

    q3 = list(df[0.75])

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df[0.00],
            line_color='firebrick',
            line_width=1,
            line_dash='dot',
            name='Minima',
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x+x_rev,
            y=q3+q1_rev,
            fill='toself',
            fillcolor='rgba(231,107,243,0.2)',
            line_color='firebrick',
            line_width=0.5,
            name='IQR',
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df[0.25],
            line_color='firebrick',
            line_width=0,
            showlegend=False,
            name='Lower Quartile',
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df[0.50],
            line_color='firebrick',
            line_width=2,
            name='Median',
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df[0.75],
            line_color='firebrick',
            line_width=0,
            showlegend=False,
            name='Upper Quartile',
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df[1.00],
            line_color='firebrick',
            line_width=1,
            line_dash='dot',
            name='Maxima',
        )
    )

    print ('ccode = {ccode}, quad = {quad}, crop = {crop}, field = {field}'.format(ccode=ccode, quad=quad, crop=crop, field=field))

    fig.update_layout(title=cropdict[crop] + ' in ' + countrydict[ccode] + ' for ' + re.sub(',',' and', quaddict[ccode][quad]),
                      xaxis_title='Year',
                      yaxis=dict(title=fielddict[field], hoverformat='.4g'),
                      hovermode='x',
                      height=550,
                      margin=dict(
                        l=50,
                        r=50,
                        b=100,
                        t=100,
                        pad=4
                      ),
                      paper_bgcolor="lightgrey"
                      )

    return fig
