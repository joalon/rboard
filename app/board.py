from app import db
from app.models import Board, Post
from flask import Blueprint
from flask import request, redirect, url_for, render_template, flash
from flask_wtf import FlaskForm


bp = Blueprint('board', __name__)


@bp.route('/create/<new_name>', methods=['GET'])
def new_board(new_name):
    newBoard = Board()
    newBoard.name = new_name
    db.session.add(newBoard)
    db.session.commit()
    return "Created new board"


@bp.route('/b/<board_name>', methods=['GET', 'POST'])
def board_index(board_name):

    board = Board.query.filter_by(name=board_name).first()
    posts = board.posts

    return render_template('board.html', title=board_name, posts=posts)

