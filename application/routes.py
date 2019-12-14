from flask import current_app as app
from flask import render_template, flash, redirect, request, url_for
from flask_login import login_user
from application.forms import LoginForm, SupportForm
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from application.student_overview import StudentOverview
app.register_blueprint(StudentOverview, url_prefix='/student/overview')

from application.student import StudentBlueprint
app.register_blueprint(StudentBlueprint, url_prefix='/student')

from application.mentor import MentorBlueprint
app.register_blueprint(MentorBlueprint, url_prefix='/mentor')

from application.mentor_overview import MentorOverview
app.register_blueprint(MentorOverview, url_prefix='/mentor/overview')

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
    form = SupportForm()
    return render_template('index.html', title='Home', form=form, **content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)