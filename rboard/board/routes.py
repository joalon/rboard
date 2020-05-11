from rboard import db
from rboard.board import blueprint
from rboard.models import Board, Post, User
from flask import request, redirect, url_for, render_template
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, validators


@blueprint.route("/create_board", methods=["GET", "POST"])
@login_required
def create_board():
    form = CreateBoardForm(request.form)

    if form.validate_on_submit():
        board = Board()
        board.name = form.name.data
        board.description = form.description.data

        user_id = current_user.get_id()
        user = User.query.get(user_id)

        board.moderators.append(user)

        db.session.add(board)
        db.session.commit()
        return redirect(url_for("board.board_index", board_name=board.name))

    return render_template("create_board.html", form=form)


@blueprint.route("/b/<board_name>", methods=["GET", "POST"])
def board_index(board_name):
    board = Board.query.filter_by(name=board_name).first()
    form = CreatePostForm(request.form)

    if current_user.is_authenticated:
        if form.validate_on_submit():
            post = Post(
                title=form.title.data,
                text=form.body.data,
                board=board,
                user=current_user,
            )
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("board.board_index", board_name=board.name))

    return render_template("board.html", board=board, form=form)


class CreateBoardForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=1, max=40)])
    description = StringField("Description", [validators.Length(min=0, max=140)])


class CreatePostForm(FlaskForm):
    title = StringField("Title", [validators.Length(min=5, max=40)])
    body = StringField("Text", [validators.Length(min=0, max=140)])
