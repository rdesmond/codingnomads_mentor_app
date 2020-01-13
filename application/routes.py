from flask import current_app as app
from flask import render_template, flash, redirect, request, url_for
from application.forms import LoginForm, SupportForm
from application import login
from flask_login import current_user, login_user, logout_user, login_required
from .models import User


from application.blueprints.student import StudentBlueprint
app.register_blueprint(StudentBlueprint, url_prefix='/student')

from application.blueprints.mentor import MentorBlueprint
app.register_blueprint(MentorBlueprint, url_prefix='/mentor')

from application.blueprints.overview import OverviewBlueprint
app.register_blueprint(OverviewBlueprint, url_prefix='/overview')

from application.blueprints.auth import AuthenticationBlueprint
app.register_blueprint(AuthenticationBlueprint)


@app.route('/')
@app.route('/index')
@login_required
def index():
    # TODO: should point to logged-in users home page. Admins -> overview/mentors, Mentors -> mentor_profile.html
    content = {
        'username': 'Miguel',
        'message': 'Welcome to your Mentor Portal!',
        'mentors': [
            {'username': 'John Doe'},
            {'username': 'Roger Doe'}
            ],
        }
    support_form = SupportForm()
    return render_template('index.html', title='Home', form=support_form, **content)
