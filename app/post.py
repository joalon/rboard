from app import db
from app.models import Board, Post, Comment, User
from flask import Blueprint
from flask import request, redirect, url_for, render_template, flash
from sqlalchemy.orm import joinedload
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, validators


bp = Blueprint("post", __name__)


@bp.route("/delete_post/<post_id>", methods=['GET'])
@login_required
def delete_post(post_id: int):
    post = Post.query.get(post_id)

    if current_user in post.board.moderators:
        board_name = post.board.name
        db.session.delete(post)
        db.session.commit()
 
        return redirect(url_for("board.board_index", board_name=board_name))


@bp.route("/b/<board_name>/<int:post_id>", methods=["POST"])
def post_index_post(board_name: str, post_id: int):
    if current_user.is_authenticated:

        reply_form = CreateCommentForm(request.form, prefix="reply")
        form = CreateCommentForm(request.form)

        if reply_form.validate_on_submit():
            parent_comment_id = request.args.get("reply_to", type=int)
            comment = Comment(text=form.body.data)

            author = User.query.get(current_user.get_id())
            parent = Comment.query.get(parent_comment_id)

            parent.comments.append(comment)
            author.comments.append(comment)

            db.session.add(comment)
            db.session.commit()

            return redirect(url_for("post.post_index", board_name=board_name, post_id=post_id))

        elif form.validate_on_submit():

            author = User.query.get(current_user.get_id())
            comment = Comment(text=form.body.data)
            post = Post.query.get(post_id)

            post.comments.append(comment)
            author.comments.append(comment)

            db.session.add(comment)
            db.session.commit()
            return redirect(url_for("post.post_index", board_name=board_name, post_id=post_id))

        return "Uh oh!"


@bp.route("/b/<board_name>/<int:post_id>", methods=["GET"])
def post_index(board_name, post_id):
    post = Post.query.options(joinedload('comments')).get(post_id)
    print(post)
    print(post.comments)
    print("children:")
    for comment in post.comments:
        print(comment.comments)
    form = CreateCommentForm(request.form)

    if request.args.get("reply_to", default=None) is not None:
        reply_form = CreateCommentForm(request.form, prefix="reply")
        return render_template("post.html", board_name=board_name, post=post,  form=form, reply_form=reply_form, comment_id=request.args.get("reply_to", type=int))

    return render_template("post.html", board_name=board_name, post=post, form=form)


@bp.route("/b/<board_name>/<int:post_id>/<int:comment_id>")
def comment(board_name, post_id, comment_id):
    print("Enter comment")
    return redirect(url_for("post.post_index", board_name=board_name, post_id=post_id, reply_to=comment_id))


class CreatePostForm(FlaskForm):
    title = StringField("Title", [validators.Length(min=5, max=40)])
    body = StringField("Text", [validators.Length(min=0, max=140)])


class CreateCommentForm(FlaskForm):
    body = StringField("Body", [validators.Length(min=1, max=140)])
