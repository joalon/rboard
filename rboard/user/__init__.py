from flask import Blueprint

blueprint = Blueprint('user', __name__)

from rboard.user import routes
