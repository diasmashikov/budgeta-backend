from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from auth.routes import *

def get_blueprint():
    return auth_bp