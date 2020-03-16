import dash_core_components as dcc
import dash_html_components as html

layout403 = html.Div([
    html.H3('Forbidden'),
    html.P("Oops! You don't have access to that"),
    dcc.Link('Return To Home', href='/')
])

layout404 = html.Div([
    html.H3('Page Not Found'),
    html.P("Sorry, what you were looking for is just not there!"),
    dcc.Link('Return To Home', href='/')
])

layout500 = html.Div([
    html.H3('Internal Error'),
    html.P("A server-side eror has been encountered"),
    html.Img(src="/static/error.jpg", alt="500 error", style={"align:middle"}),
    html.P('''
    It would be really helpful to shoot me an email telling me about this: [cemac-help@leeds.ac.uk](mailto:cemac-help@leeds.ac.uk) or [c.c.symonds@leeds.ac.uk](mailto:c.c.symonds@leeds.ac.uk)
    ''', style={"text-align: center"}
    ),
    dcc.Link('Return To Home', href='/')
])

layout501 = html.Div([
    html.H3('Unhandled Error'),
    html.P("Hey! You broke the website!"),
    html.Img(src="/static/error.jpg", alt="500 error", style={"align:middle!"}),
    html.P('''
    Not, really you just caught an error! It would be really helpful to shoot me an email telling me about this: [cemac-help@leeds.ac.uk](mailto:cemac-help@leeds.ac.uk) or [c.c.symonds@leeds.ac.uk](mailto:c.c.symonds@leeds.ac.uk)
    ''', style={"text-align: center"}
    ),
    dcc.Link('Return To Home', href='/')
])
