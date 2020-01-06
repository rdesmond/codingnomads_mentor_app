import json

from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for, abort
from application.utils import utc_to_local
from application import db
from application.models import User, Mentor, Student, Course, SupportLog, UserCourse
from application.forms import SupportForm
from application.data_services import get_student_info, log_student_support

StudentBlueprint = Blueprint('student', __name__)

# Returns details about a given student including name ,goals, availability, local time, progress, notes and support log
@StudentBlueprint.route('/<student_id>', methods=['GET'])
def get_student(student_id):

    # Get info from DB
    data = get_student_info(student_id)

    if data is None:
        return abort(404, description='Student not found')

    # TODO: change to proper backend calls
    form = SupportForm()
    content = json.loads("""{
    "current_user": {
        "first_name": "Gilad",
        "last_name": "Gressel",
        "is_admin": false,
        "user_id": 1
    },
    "student": {
        "aims": "wants to learn to frontend",
        "id": 2,
        "mentor_id": 3,
        "mentor_name": "Gilad Gressel",
        "preferred_learning": "discussions",
        "start_date": "Fri, 13 Sep 2019 13:14:57 GMT",
        "status": "student",
        "user_id": 2,
        "username": "johnny",
        "email": "johnny@gmail.com",
        "first_name": "Johnny",
        "last_name": "Appleseed",
        "learning_platform": "jseed",
        "forum": "johnny",
        "slack": "apple",
        "time_zone": "Europe/London",
        "courses": [
            {
                "id": 8,
                "name": "Python Software Development",
                "progress_percent": 80
            }
        ],
        "preferred_days": {
            "Mon": true, "Tue": true, "Wed": true,
            "Thu": true, "Fri": true, "Sat": false, "Sun": false},
        "preferred_start_time": "08:00:00",
        "preferred_end_time": "17:00:00"
    }
}
    """)
    return render_template('student_profile.html', form=form, title=content['student']['username'], **content)
    # return jsonify(data), 200


# Log support for a given student
@StudentBlueprint.route('/support/<student_id>', methods=['POST'])
def log_support_student(student_id):  # TODO: input could be mentor_id from currently logged in user (+add below)

    form = SupportForm()
    if form.validate_on_submit():
        flash('Support Log submitted for student #{} by mentor #{}'.format(
            form.mentor_id.data, form.student_id.data))

        # Create a row in the support log table
        mentor_id = request.form['mentor_id']  # TODO: this should come from the authenticated_user
        student_id = request.form['student_id']
        support_type = request.form['support_type']
        time_spent = request.form['time_spent']
        notes = request.form['notes']
        comprehension = request.form['comprehension']

        log_student_support(mentor_id,
            student_id,
            support_type,
            time_spent,
            notes,
            comprehension)
            
    else:
        flash('Missing data. Please fill all the fields')
    return redirect(url_for('index'))


