from flask import Blueprint

category_bp = Blueprint('category', __name__)

from category.routes import *

def get_blueprint():
    return category_bp