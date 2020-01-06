from flask import Blueprint, jsonify, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select
from sqlalchemy import text

from application import db
from application.models import User, Mentor, Student, Course, SupportLog, UserCourse
from application.data_services import get_mentor_info, log_student_support
from application.forms import SupportForm
import json

MentorBlueprint = Blueprint('mentor', __name__)


base_content = json.loads("""{
        "current_user": {
            "first_name": "Gilad",
            "last_name": "Gressel",
            "is_admin": false,
            "user_id": 1
        },
        "mentor": {
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
            "slack": "UGLT4QR9N",
            "time_zone": "America/Los_Angeles",
            "preferred_days": {
                "Mon": true, "Tue": false, "Wed": true,
                "Thu": true, "Fri": true, "Sat": false, "Sun": false},
            "preferred_start_time": "08:00",
            "preferred_end_time": "17:00"
        }
    }
    """)

# Returns details about a given mentor including name, current students / spare capacity, availability, local time, assigned students, notes, support log
@MentorBlueprint.route('/<mentor_id>', methods=['GET'])
def get_mentor(mentor_id):

    # Get info from DB
    data = get_mentor_info(mentor_id)

    if data is None:
        return abort(404, 'Mentor not found')

    # TODO: change to proper backend calls
    form = SupportForm()
    content = base_content
    return render_template('mentor_profile.html', form=form, title=content['mentor']['username'], **content)
    # return jsonify(data), 200


# Log support for a given student
@MentorBlueprint.route('/<mentor_id>/<student_id>', methods=['POST'])
def student_log_support(mentor_id):

    # # Code for when a form is built on the front end
    # mentor_id = request.form['mentor_id']
    # support_type = request.form['support_type']
    # time_spent = request.form['support_type']
    # notes = request.form['notes']
    # comprehension = request.form['comprehension']

    mentor_id = mentor_id
    student_id = 3
    support_type = 'test'
    time_spent = 5
    notes = 'test'
    comprehension = 5

    # Create a row in the support log table

    log_student_support(
        mentor_id=mentor_id,
        student_id=student_id,
        support_type=support_type,
        time_spent=time_spent,
        notes=notes,
        comprehension=comprehension
    )

    return "Success"


@MentorBlueprint.route('/<mentor_id>/students', methods=['GET'])
def get_mentored_students(mentor_id):
    # TODO: change to proper backend calls
    form = SupportForm()
    content = dict(base_content, **json.loads("""{
    "students": [
        {
            "aims": "wants to learn to frontend",
            "id": 2,
            "mentor_id": 3,
            "preferred_learning": "discussions",
            "start_date": "Fri, 13 Sep 2019 13:14:57 GMT",
            "status": "alumni",
            "user_id": 2,
            "username": "carol",
            "email": "johnny@gmail.com",
            "first_name": "Carol",
            "last_name": "Dunlop",
            "learning_platform": "carol",
            "forum": "carol",
            "slack": "apple",
            "time_zone": "America/Los_Angeles",
            "courses": [
                {
                    "id": 8,
                    "name": "Python Software Development",
                    "progress_percent": 100
                }
            ],
            "next_call": "Thu, 22 Sep 2019 13:14:57 GMT"
        },
        {
            "aims": "get a job asap",
            "id": 4,
            "mentor_id": 3,
            "preferred_learning": "military study",
            "start_date": "Fri, 13 Sep 2019 13:14:57 GMT",
            "status": "student",
            "user_id": 7,
            "username": "larry",
            "email": "larry@gmail.com",
            "first_name": "Larry",
            "last_name": "Longbottom",
            "learning_platform": "larry",
            "forum": "llong",
            "slack": "larrylong",
            "time_zone": "Europe/London",
            "courses": [
                {
                    "id": 8,
                    "name": "Python Software Development",
                    "progress_percent": 10
                }
            ],
            "next_call": "Fri, 23 Sep 2019 13:14:57 GMT"
        }
    ]
}
"""))
    return render_template('mentor_students.html', form=form, title=content['mentor']['username'], **content)
    # return jsonify(data), 200


@MentorBlueprint.route('/<mentor_id>/notes', methods=['GET'])
def get_mentor_notes(mentor_id):
    # TODO: change to proper backend calls
    form = SupportForm()
    content = dict(base_content, **json.loads("""{
    "notes": [
        {
            "mentor_id": 3,
            "student_id": 7,
            "text": "this is an example note.",
            "timestamp": "Fri, 23 Sep 2019 13:14:57 GMT"
        },
        {
            "mentor_id": 3,
            "student_id": 2,
            "text": "another example note.",
            "timestamp": "Thu, 22 Sep 2019 13:14:57 GMT"
        }
    ]
}"""))
    return render_template('mentor_notes.html', form=form, title=content['mentor']['username'], **content)

