import numpy as np
import re
import xarray as xr
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from Applications.DashApp.axisdicts import countrydict, cropdict, fielddict, quaddict, rcpdict, unitdict

DATA_PATH = "/var/www/production/data"
#DATA_PATH = "./data"

def get_cubedata(ccode, quad, crop, field):

    import os
    import pandas as pd

    if ccode == None:
        ccode = "MWI"

    if field == None:
        field = 'yield'

    if quad==None:
        quad='00'

    if ccode == 'MWI':
        if quad == '01':
            rcp=2
            irr_lev=0.1
        elif quad == '10':
            rcp=0
            irr_lev=0
        elif quad == '11':
            rcp=2
            irr_lev=0
        else:
            rcp=0
            irr_lev=0.1
    elif ccode == 'TZA':
        if quad == '01':
            rcp=2
            irr_lev=0.1
        elif quad == '10':
            rcp=0
            irr_lev=0
        elif quad == '11':
            rcp=2
            irr_lev=0
        else:
            rcp=0
            irr_lev=0.1
    elif ccode == 'ZAF':
        if quad == '01':
            rcp=2
            irr_lev=0.1
        elif quad == '10':
            rcp=0
            irr_lev=0
        elif quad == '11':
            rcp=2
            irr_lev=0.1
        else:
            rcp=0
            irr_lev=0
    else:
        if quad == '01':
            rcp=2
            irr_lev=0.1
        elif quad == '10':
            rcp=0
            irr_lev=0
        elif quad == '11':
            rcp=2
            irr_lev=0
        else:
            rcp=0
            irr_lev=0.1

    ds = None

    if ccode == 'ZAF':
        countrystr='safrica'
    else:
        countrystr=countrydict[ccode].lower()

    fname = os.path.join(DATA_PATH,countrystr+"_"+cropdict[crop].lower()+"_"+rcpdict[rcp]+".nc")

    if not os.path.exists(fname):
        print('Could not load file '+fname)

    try:
        ds = xr.open_dataset(fname, decode_cf=False)
        # decode_cf flag needed so data types aren't automatically chosen from units

        da = ds[field].loc[dict(rcp=rcp, irr_lev=irr_lev)]
        da = da.where((da <= 1e+20))
    except:
        if ds: ds.close()
        try:
            ds = xr.open_dataset(fname)

            da = ds[field].loc[dict(rcp=rcp, irr_lev=irr_lev)]
            da = da.where((da <= 1e+20))
        except:
            dflst = []
            linedf = pd.DataFrame(np.zeros((99,5)))
            box1df = pd.DataFrame(np.zeros((18,21)))
            box2df = pd.DataFrame(np.zeros((18,21)))
            linedf.columns = [0.0, 0.25, 0.5, 0.75, 1.0]
            box1df.columns = [x for x in range (1990,2011)]
            box2df.columns = [x for x in range (2040,2061)]

            dflst=[linedf, box1df, box2df]

            return dflst

    weights = np.cos(np.deg2rad(da.lat))
    if field == "yield" or field == "biomass":
        weighted = da.weighted(weights).mean(("lon","lat"), skipna=True)
    else:
        weighted = da.weighted(weights).mean(("lon","lat"), skipna=True)

    dflst = []

    if crop == 0 or crop == 2:
        prod_lev = 0.1
    elif crop == 3:
        if ccode == 'ZMB':
            prod_lev = 0.7
        else:
            prod_lev = 0.6
    elif crop == 1:
        if ccode == 'ZAF':
            prod_lev = 0.3
        else:
            prod_lev = 0.2

    df = weighted.loc[dict(crop=crop, prod_lev=prod_lev)].to_pandas()

    linedf = df.quantile(q=[0.0, 0.25, 0.5, 0.75, 1.0], axis=1).T
    box1df = df.iloc[0:21,:].T
    box2df = df.iloc[50:71,:].T

    dflst = [linedf, box1df, box2df]

    ds.close()

    return dflst


def get_cubedata2(ccode, irr_lev, prod_lev, rcp, crop, field):

    import os
    import pandas as pd

    if ccode == None:
        ccode = "MWI"

    if field == None:
        field = 'yield'

    if irr_lev == None:
        irr_lev = 0

    if crop == None:
        crop = 2

    if prod_lev == None:
        if crop == 0 or crop == 2:
            prod_lev = 0.1
        elif crop == 3:
            if ccode == 'ZMB':
                prod_lev = 0.7
            else:
                prod_lev = 0.6
        elif crop == 1:
            if ccode == 'ZAF':
                prod_lev = 0.3
            else:
                prod_lev = 0.2

    ds = None

    if ccode == 'ZAF':
        countrystr='safrica'
    else:
        countrystr=countrydict[ccode].lower()

    fname = os.path.join(DATA_PATH,countrydict[ccode].lower()+"_"+cropdict[crop].lower()+"_"+rcpdict[rcp]+".nc")

    if not os.path.exists(fname):
        print('Could not load file '+fname)

    try:
        ds = xr.open_dataset(fname, decode_cf=False)
        # decode_cf flag needed so data types aren't automatically chosen from units

        da = ds[field].loc[dict(rcp=rcp, irr_lev=irr_lev, prod_lev=prod_lev, crop=crop)]
        da = da.where((da <= 1e+20))
    except:
        if ds: ds.close()
        try:
            ds = xr.open_dataset(fname)

            da = ds[field].loc[dict(rcp=rcp, irr_lev=irr_lev, prod_lev=prod_lev, crop=crop)]
            da = da.where((da <= 1e+20))
        except:
            dflst = []
            linedf = pd.DataFrame(np.zeros((99,5)))
            box1df = pd.DataFrame(np.zeros((18,21)))
            box2df = pd.DataFrame(np.zeros((18,21)))
            linedf.columns = [0.0, 0.25, 0.5, 0.75, 1.0]
            box1df.columns = [x for x in range (1990,2011)]
            box2df.columns = [x for x in range (2040,2061)]

            dflst.append([linedf, box1df, box2df])

            return dflst

    weights = np.cos(np.deg2rad(da.lat))
    if field == "yield" or field == "biomass":
        weighted = da.weighted(weights).mean(("lon","lat"), skipna=True)
    else:
        weighted = da.weighted(weights).mean(("lon","lat"), skipna=True)

    dflst = []

    df = weighted.to_pandas()

    linedf = df.quantile(q=[0.0, 0.25, 0.5, 0.75, 1.0], axis=1).T
    box1df = df.iloc[0:21,:].T
    box2df = df.iloc[50:71,:].T

    dflst = [linedf, box1df, box2df]

    ds.close()

    return dflst


def cropgraph(ccode, quad, crop, croplst, field):

    if quad==None:
        quad='00'

    df = croplst[0]
    dfbox1 = croplst[1]
    dfbox2 = croplst[2]

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
            y=dfbox1.to_numpy().flatten(),
            name=int(list(dfbox1.columns)[10]),
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
            y=dfbox2.to_numpy().flatten(),
            name=list(dfbox2.columns)[10],
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
                      paper_bgcolor="White",)

    return fig


def cropgraph2(ccode, clim, crop, croplst, field):

    if clim==None:
        clim='Low'

    df = croplst[0]
    dfbox1 = croplst[1]
    dfbox2 = croplst[2]

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
            y=dfbox1.to_numpy().flatten(),
            name=int(list(dfbox1.columns)[10]),
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
            y=dfbox2.to_numpy().flatten(),
            name=list(dfbox2.columns)[10],
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
    fig.update_yaxes(title_text=fielddict[field]+unitdict[field], hoverformat='.4g', row=1, col=2)

    fig.update_layout(title=cropdict[crop] + ' in ' + countrydict[ccode] + ' for ' +clim+' Climate Risk',
                      xaxis_title='Year',
                      yaxis=dict(title=fielddict[field]+unitdict[field], hoverformat='.4g'),
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


def compgraph(ccode, rcp, crop, croplst, field):

    df = croplst[0]
    #dfbox = croplst[crop][1]

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


    if rcp == 0:
        climstr = "Low Climate Risk"
    else:
        climstr = "High Climate Risk"

    fig.update_layout(title=cropdict[crop] + ' in ' + countrydict[ccode] + ' for ' + climstr,
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
