from flask import Blueprint

blueprint = Blueprint('main', __name__)

from rboard.main import routes
