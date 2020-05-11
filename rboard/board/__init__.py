from flask import Blueprint

blueprint = Blueprint('board', __name__)

from rboard.board import routes
