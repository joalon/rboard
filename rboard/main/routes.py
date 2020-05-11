from rboard import db
from rboard.models import Board
from rboard.main import blueprint
from flask import request, redirect, url_for, render_template, flash
from flask_login import current_user


@blueprint.route("/", methods=["GET"])
def index():
    boards = Board.query.all()
    return render_template("main.html", boards=boards)
