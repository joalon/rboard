from flask import Flask, Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect


bp = Blueprint("base", __name__)
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
csrf = CSRFProtect()


def make_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SECRET_KEY'] = 'Bad_idea 123'

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    csrf.init_app(app)

    app.register_blueprint(bp)

    from app.user import bp as user_bp
    app.register_blueprint(user_bp)

    from app.board import bp as board_bp
    app.register_blueprint(board_bp)

    return app


@bp.route("/")
def index():
    return render_template('base.html')


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from app.models import User
