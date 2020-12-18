"""Application entry point for ifeed01."""
from Applications.DashApp.dashindex import app

import sys

path = "/var/www/development/"

if path not in sys.path:
    sys.path.append(path)

application = app.server
