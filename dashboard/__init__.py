from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__)

from dashboard.routes import *

def get_blueprint():
    return dashboard_bp