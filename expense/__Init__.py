from flask import Blueprint

expense_bp = Blueprint('expense', __name__)

from expense.routes import *

def get_blueprint():
    return expense_bp