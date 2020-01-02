import json
from flask import current_app as app
from flask import render_template, flash, redirect, request, url_for
from flask_login import login_user
from application.forms import LoginForm, SupportForm
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from application import login
from flask_login import current_user, login_user, logout_user, login_required
from .models import User

from application.blueprints.student_overview import StudentOverviewBlueprint
app.register_blueprint(StudentOverviewBlueprint, url_prefix='/student/overview')

from application.blueprints.student import StudentBlueprint
app.register_blueprint(StudentBlueprint, url_prefix='/student')

from application.blueprints.mentor import MentorBlueprint
app.register_blueprint(MentorBlueprint, url_prefix='/mentor')

from application.blueprints.mentor_overview import MentorOverviewBlueprint
app.register_blueprint(MentorOverviewBlueprint, url_prefix='/mentor/overview')

from application.blueprints.auth import AuthenticationBlueprint
app.register_blueprint(AuthenticationBlueprint)


@app.route('/')
@app.route('/index')
@login_required
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


# TODO: change this to actual backend call
@app.route('/mentors')
def show_mentor_list():
    form = SupportForm()
    content = json.loads("""{
    "current_user":{
        "first_name": "Ryan",
        "last_name": "Desmond",
        "is_admin": true
    },
    "mentors": [
        {
            "completed_students": 5,
            "current_students": 0,
            "id": 3,
            "is_admin": false,
            "max_students": 3,
            "rating": 5,
            "user_id": 1,
            "username": "gilad",
            "email": "gilad@gmail.com",
            "first_name": "Gilad",
            "last_name": "Gressel",
            "learning_platform": "gilad",
            "forum": "gilad",
            "slack": "gilad",
            "time_zone": "America/Los_Angeles",
            "last_support_log_created": "2020-01-01 11:19:06.782213"
        },
        {
            "completed_students": 6,
            "current_students": 1,
            "id": 2,
            "is_admin": true,
            "max_students": 5,
            "rating": 4,
            "user_id": 2,
            "username": "martin",
            "email": "breuss.martin@gmail.com",
            "first_name": "Martin",
            "last_name": "Breuss",
            "learning_platform": "martin",
            "forum": "martin",
            "slack": "Martin Breuss",
            "time_zone": "Europe/Vienna",
            "last_support_log_created": "2019-12-14 15:19:06.782213"
        }
    ]
}
""")
    return render_template('mentor_overview.html', form=form, title='Mentors', **content)