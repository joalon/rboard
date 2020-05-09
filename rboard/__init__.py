import os
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

    if app.config['ENV'] == 'dev':
        print("Starting in dev")
        app.config.from_pyfile('config/dev.cfg')
    elif app.config['ENV'] == 'prod':
        print("Starting in prod")
        app.config.from_pyfile('config/prod.cfg')
    else:
        print("Expected FLASK_ENV to be either 'prod' or 'dev'")
        exit(1)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    csrf.init_app(app)

    app.register_blueprint(bp)

    from rboard.main import bp as main_bp
    app.register_blueprint(main_bp)

    from rboard.user import bp as user_bp
    app.register_blueprint(user_bp)

    from rboard.board import bp as board_bp
    app.register_blueprint(board_bp)

    from rboard.post import bp as post_bp
    app.register_blueprint(post_bp)

    return app


app = make_app()


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from rboard.models import User
