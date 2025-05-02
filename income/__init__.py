from flask import Blueprint

income_bp = Blueprint('income', __name__)

from income.routes import *

def get_blueprint():
    return income_bp