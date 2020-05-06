from app import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    passwordHash = db.Column(db.String(100))
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship("Post", backref="user")
    comments = db.relationship("Comment", backref="user")

    def check_password(self, password):
        return check_password_hash(self.passwordHash, password)

    def __repr__(self):
        return f"<User '{self.username}'>"

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.id == other.id
        return False


moderators = db.Table(
    "moderators",
    db.Column("moderator_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("board_id", db.Integer, db.ForeignKey("board.id")),
)


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    description = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    posts = db.relationship(
        "Post", backref="board", order_by="Post.posted_at.desc()"
    )

    moderators = db.relationship("User", secondary=moderators)

    def __repr__(self):
        return f"<Board '{self.name}'>"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    text = db.Column(db.String(140))
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"))

    comments = db.relationship(
        "Comment", backref="post"
    )

    def __repr__(self):
        return f"<Post '{self.title}'>"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140))
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    parent_comment_id = db.Column(db.Integer, db.ForeignKey("comment.id"))

    comments = db.relationship(
        "Comment", backref="parent_comment", remote_side=[id]
    )

    def __repr__(self):
        return f"<Comment '{self.id}'>"
