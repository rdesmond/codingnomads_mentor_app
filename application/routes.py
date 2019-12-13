from flask import current_app as app
from flask import render_template, flash, redirect
from application.forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from application.student_overview import StudentOverview
app.register_blueprint(StudentOverview, url_prefix='/student/overview')

from application.student import Student
app.register_blueprint(Student, url_prefix='/student')

from application.mentor import Mentor
app.register_blueprint(Mentor, url_prefix='/mentor')

from application.mentor_overview import MentorOverview
app.register_blueprint(MentorOverview, url_prefix='/mentor/overview')

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John Doe'},
            'body': 'Welcome to your Mentor Portal!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)