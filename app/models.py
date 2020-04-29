from app import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    passwordHash = db.Column(db.String(100))
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def check_password(self, password):
        return check_password_hash(self.passwordHash, password)

    def __repr__(self):
        return f"<User '{self.username}'>"


moderators = db.Table('moderators',
    db.Column('moderator_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('board_id', db.Integer, db.ForeignKey('board.id'))
)


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    description = db.column(db.String(100))
    posts = db.relationship('Post', backref='board', lazy='dynamic')

    moderators = db.relationship(
        'User', secondary=moderators,
        primaryjoin=(moderators.c.moderator_id == id),
        secondaryjoin=(moderators.c.board_id == id),
        backref=db.backref('moderator_for', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return f"<Board '{self.name}'>"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), unique=True)
    text = db.Column(db.String(140))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"))

    def __repr__(self):
        return f"<Post '{self.title}'>"

