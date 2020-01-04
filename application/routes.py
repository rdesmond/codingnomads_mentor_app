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
            "learning_platform": 70,
            "forum": "gilad",
            "slack": "UGLT4QR9N",
            "time_zone": "America/Los_Angeles",
            "last_support_log_created": "2020-01-01 11:19:06.782213"
        },
        {
            "completed_students": 6,
            "current_students": 3,
            "id": 2,
            "is_admin": true,
            "max_students": 5,
            "rating": 4,
            "user_id": 2,
            "username": "martin",
            "email": "breuss.martin@gmail.com",
            "first_name": "Martin",
            "last_name": "Breuss",
            "learning_platform": 25,
            "forum": "martin",
            "slack": "UGL5A5X18",
            "time_zone": "Europe/Vienna",
            "last_support_log_created": "2019-12-14 15:19:06.782213"
        }
    ]
}
""")
    return render_template('mentor_overview.html', form=form, title='Mentors', **content)


# TODO: change this to actual backend call
@app.route('/students')
def show_student_list():
    form = SupportForm()
    content = json.loads("""{
    "current_user":{
        "first_name": "Ryan",
        "last_name": "Desmond",
        "is_admin": true
    },
    "students": [
        {
            "aims": "wants to learn to frontend",
            "id": 2,
            "mentor_id": 3,
            "mentor_name": "Gilad Gressel",
            "preferred_learning": "discussions",
            "start_date": "Fri, 13 Sep 2019 13:14:57 GMT",
            "status": "alumni",
            "user_id": 2,
            "username": "carol",
            "email": "carol@gmail.com",
            "first_name": "Carol",
            "last_name": "Denvers",
            "learning_platform": "jseed",
            "forum": "coral",
            "slack": "apple",
            "time_zone": "Europe/London",
            "courses": [
                {
                    "id": 8,
                    "name": "Python Software Development",
                    "progress_percent": 90
                }
            ]
        },
        {
            "aims": "get a job asap",
            "id": 4,
            "mentor_id": null,
            "mentor_name": null,
            "preferred_learning": "military study",
            "start_date": "Fri, 13 Sep 2019 13:14:57 GMT",
            "status": "hot lead",
            "user_id": 7,
            "username": "larry",
            "email": "larry@gmail.com",
            "first_name": "Larry",
            "last_name": "Longbottom",
            "learning_platform": "larry",
            "forum": "llong",
            "slack": "larrylong",
            "time_zone": "Africa/Addis_Ababa",
            "courses": [
                {
                    "id": 8,
                    "name": "Python Software Development",
                    "progress_percent": 0
                }
            ]
        }
    ]
}
""")
    return render_template('student_overview.html', form=form, title='Students', **content)