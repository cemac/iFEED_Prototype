"""Initialize app."""
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import flask
from Applications.DashApp.dashadds import *
from Applications.FlaskApp.errorpages import *
from Applications.DashApp.mainlayout import CustomDash
#from Applications.DashApp.dataviz import *
#from Applications.DashApp.callbacks import *

"""Construct the core application."""

fl_app = Flask(__name__,
               instance_relative_config=False)

fl_app.config.from_object('Applications.config.Config')

with fl_app.app_context():

    # Import main Blueprint
    from Applications.FlaskApp.flask_app import main_bp
    fl_app.register_blueprint(main_bp)

    # Import Error Pages
    fl_app.register_error_handler(404,page_not_found)
    fl_app.register_error_handler(403,page_not_allowed)
    fl_app.register_error_handler(500,internal_error)
    fl_app.register_error_handler(501,unhandled_exception)

    # Compile assets
    from Applications.assets import compile_assets
    compile_assets(fl_app)

# Import Dash application
app = CustomDash(server=fl_app,
                 external_stylesheets=external_stylesheets,
                 external_scripts=external_scripts,
                 meta_tags=meta_tags,
                 requests_pathname_prefix='/data_exploration/',
                 routes_pathname_prefix='/data_exploration/'
                 )
server = app.server
app.config.suppress_callback_exceptions = True
