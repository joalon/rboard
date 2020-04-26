from flask import Flask, Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate




bp = Blueprint("main", __name__)
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()


def make_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(bp)

    from app.user import bp as user_bp

    app.register_blueprint(user_bp)
    return app


@bp.route("/")
def index():
    return render_template('base.html')


from app.models import User
