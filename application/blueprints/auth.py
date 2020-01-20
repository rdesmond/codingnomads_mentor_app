from flask import Blueprint,render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from application.forms import LoginForm, ChangePasswordForm
from application.models import User
from application import db


AuthenticationBlueprint = Blueprint('auth', __name__)


@AuthenticationBlueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        print(user)
        if user is None or not user.check_password(login_form.password.data):
            flash('Login requested for user {}, remember_me={}'.format(login_form.username.data,
                                                                       login_form.remember_me.data))
            return redirect(url_for('login'))
        login_user(user)
        if current_user.is_admin:
            return redirect(url_for('overview.show_mentor_list'))
        elif current_user.is_mentor:
            return redirect(url_for('mentor.get_mentor', mentor_id=current_user.mentor.id))
    return render_template('login.html', title='Sign In', login_form=login_form)


@AuthenticationBlueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@AuthenticationBlueprint.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    user = current_user
    if form.validate_on_submit():
        if not user.check_password(form.current_password.data):
            flash('Current Password is incorrect')
            return redirect(url_for('/change_password'))
        user.password_hash = user.set_password(form.new_password.data)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('change_password.html', form=form)
