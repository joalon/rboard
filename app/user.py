from app import db
from app.models import User
from flask import Blueprint
from flask import request, redirect, url_for, render_template, flash
from flask_wtf import FlaskForm
from flask_login import logout_user, current_user, login_user, UserMixin, login_required
from wtforms import StringField, PasswordField, validators
from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint('user', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    print("Got login request")
    if current_user.is_authenticated:
        print("already logged in")
        redirect(url_for('index'))

    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            print("Found user: " + str(user))
            login_user(user)
            print(current_user.is_authenticated)
            return redirect(url_for('user.users'))
        print("user not found")

    print("form invalid:")
    print(str(form.errors))
    return render_template('login.html', title="Sign in", form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base.index'))


@bp.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', title='Users', users=users)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(username=form.username.data,
                        passwordHash=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('base.index'))
    return render_template('register.html', form=form)


class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=1, max=40)])
    password = PasswordField('New Password', [validators.Length(min=3, max=100)])


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=1, max=40)])
    password = PasswordField('Password', [validators.Length(min=3, max=100)])
