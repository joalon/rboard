from flask import Blueprint

blueprint = Blueprint('post', __name__)

from rboard.post import routes
