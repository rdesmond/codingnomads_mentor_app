from flask import current_app as app
from flask import render_template, flash, redirect, request, url_for
from flask_login import login_user
from application.forms import LoginForm, SupportForm
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from application import login
from flask_login import current_user, login_user, logout_user, login_required
from .models import User

from application.student_overview import StudentOverviewBlueprint
app.register_blueprint(StudentOverviewBlueprint, url_prefix='/student/overview')

from application.student import StudentBlueprint
app.register_blueprint(StudentBlueprint, url_prefix='/student')

from application.mentor import MentorBlueprint
app.register_blueprint(MentorBlueprint, url_prefix='/mentor')

from application.mentor_overview import MentorOverviewBlueprint
app.register_blueprint(MentorOverviewBlueprint, url_prefix='/mentor/overview')

from application.auth import AuthenticationBlueprint
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

