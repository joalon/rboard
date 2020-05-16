from rboard import db
from rboard.user import blueprint
from rboard.models import User
from flask import request, redirect, url_for, render_template, flash
from flask_wtf import FlaskForm
from flask_login import logout_user, current_user, login_user, UserMixin, login_required
from wtforms import StringField, PasswordField, validators
from werkzeug.security import generate_password_hash, check_password_hash


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        redirect(url_for('index'))

    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))

    return render_template('login.html', title="Sign in", form=form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(username=form.username.data,
                        passwordHash=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
    return render_template('register.html', form=form)


class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=1, max=40)])
    password = PasswordField('New Password', [validators.Length(min=3, max=100)])


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=1, max=40)])
    password = PasswordField('Password', [validators.Length(min=3, max=100)])
