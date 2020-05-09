from rboard import db
from rboard.models import Board
from flask import Blueprint
from flask import request, redirect, url_for, render_template, flash
from flask_login import current_user


bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET"])
def index():

    boards = Board.query.all()

    return render_template("main.html", boards=boards)
