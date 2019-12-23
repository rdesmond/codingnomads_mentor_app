from flask import Blueprint,render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from application.forms import LoginForm, ChangePasswordForm
from application.models import User
from . import db


AuthenticationBlueprint = Blueprint('auth', __name__)


@AuthenticationBlueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
            return redirect(url_for('index'))
        login_user(user)
    return render_template('login.html', title='Sign In', form=form)



@AuthenticationBlueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@AuthenticationBlueprint.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    
    form = ChangePasswordForm()
    user = current_user

    if form.validate_on_submit():
        if not user.check_password(form.current_password.data):
            flask('Current Password is incorrect')
            return redirect(url_for('/change_password'))
        user.password_hash = user.set_password(form.new_password.data)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('change_password.html', form=form)
