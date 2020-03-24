import dash_html_components as html
from Applications.DashApp import dataviz

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
                 children=dataviz.testcrop(ccode, quad))
    ])

    return layout
