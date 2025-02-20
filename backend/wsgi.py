"""
WSGI configuration for PythonAnywhere deployment.
This file should be placed in the same directory as your main.py
"""

import os
import sys

# Add the project directory to the sys.path
project_home = os.path.expanduser('~/kuakuaqun_web/backend')
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['ENVIRONMENT'] = 'production'

# Import the FastAPI application
from main import app

# Create the WSGI application
from fastapi.middleware.wsgi import WSGIMiddleware
application = WSGIMiddleware(app) 