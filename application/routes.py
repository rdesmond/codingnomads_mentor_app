from flask import current_app as app
from flask import render_template, flash, redirect
from application.forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

from application import login 

from application.student_overview import StudentOverviewBlueprint
app.register_blueprint(StudentOverviewBlueprint, url_prefix='/student/overview')

from application.student import StudentBlueprint
app.register_blueprint(StudentBlueprint, url_prefix='/student')

from application.mentor import MentorBlueprint
app.register_blueprint(MentorBlueprint, url_prefix='/mentor')

from application.mentor_overview import MentorOverviewBlueprint
app.register_blueprint(MentorOverviewBlueprint, url_prefix='/mentor/overview')

@app.route('/')
@app.route('/index')
def index():
    content = {
        'username': 'Miguel',
        'message': 'Welcome to your Mentor Portal!',
        'mentors': [
            {'username': 'John Doe'},
            {'username': 'Roger Doe'}
            ],
        }
    return render_template('index.html', title='Home', **content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))