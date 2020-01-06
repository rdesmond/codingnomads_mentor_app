import json

from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for, abort
from application.utils import utc_to_local
from application import db
from application.models import User, Mentor, Student, Course, SupportLog, UserCourse
from application.forms import SupportForm
from application.data_services import get_student_info, log_student_support

StudentBlueprint = Blueprint('student', __name__)

base_content = json.loads("""{
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
        "first_name": "Carol",
        "last_name": "Dunlop",
        "learning_platform": "carol",
        "forum": "carol",
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
        "preferred_start_time": "08:00",
        "preferred_end_time": "12:00"
    }
}
    """)


# Returns details about a given student including name ,goals, availability, local time, progress, notes and support log
@StudentBlueprint.route('/<student_id>', methods=['GET'])
def get_student(student_id):

    # Get info from DB
    data = get_student_info(student_id)

    if data is None:
        return abort(404, description='Student not found')

    # TODO: change to proper backend calls
    form = SupportForm()
    content = base_content
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


@StudentBlueprint.route('/<student_id>/logs', methods=['GET'])
def get_student_logs(student_id):

    # TODO: change to proper backend calls
    form = SupportForm()
    content = dict(base_content, **json.loads("""{
    "support_logs": [
        {
            "mentor_id": 3,
            "student_id": 7,
            "notes": "this is an example note for a support log.",
            "created_at": "Fri, 23 Sep 2019 13:14:57 GMT",
            "support_type": "call",
            "time_spent": 40,
            "comprehension": 5
        },
        {
            "mentor_id": 3,
            "student_id": 7,
            "notes": "call went well, we discussed exceptions.",
            "created_at": "Fri, 23 Sep 2019 13:14:57 GMT",
            "support_type": "call",
            "time_spent": 30,
            "comprehension": 5
        }
    ]
}
"""))
    return render_template('student_logs.html', form=form, title=content['student']['username'], **content)


@StudentBlueprint.route('/<student_id>/progress', methods=['GET'])
def get_student_progress(student_id):
    # TODO: change to proper backend calls
    form = SupportForm()
    content = dict(base_content, **json.loads("""{
    "progress": [
        {
            "course_id": 8,
            "course_name": "Python Software Development",
            "progress_percent": 80,
            "last_access": "timestamp here",
            "last_page_accessed_id": 203,
            "last_page_accessed_name": "Conditionals Overview",
            "furthest_page_accessed_id": 274,
            "furthest_page_accessed_name": "Intro to Exceptions",
            "furthest_section_name": "Exceptions",
            "furthest_section_current_resource": 2,
            "furthest_section_total_resources": 7
        }

    ]
}
"""))
    return render_template('student_progress.html', form=form, title=content['student']['username'], **content)


@StudentBlueprint.route('/<student_id>/notes', methods=['GET'])
def get_student_notes(student_id):
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
            "student_id": 7,
            "text": "another example note for the same student.",
            "timestamp": "Thu, 22 Sep 2019 13:14:57 GMT"
        },
        {
            "mentor_id": 4,
            "student_id": 7,
            "text": "another example note for the same student but taken by a different mentor.",
            "timestamp": "Thu, 22 Sep 2019 13:14:57 GMT"
        }
    ]
}
"""))
    return render_template('student_notes.html', form=form, title=content['student']['username'], **content)
