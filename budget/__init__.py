from flask import Blueprint

budget_bp = Blueprint('budget', __name__)

from budget.routes import *

def get_blueprint():
    return budget_bp