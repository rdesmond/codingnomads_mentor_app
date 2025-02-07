import json
from flask import Blueprint, render_template, abort
from flask_login import current_user, login_required
from application.forms import SupportForm
from application.data_services import get_student_info, get_student_support_logs, get_student_notes_by_student


StudentBlueprint = Blueprint('student', __name__)


base_content = json.loads("""{
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
base_content['current_user'] = current_user


@StudentBlueprint.route('/<user_id>', methods=['GET'])
@login_required
def get_student(user_id):
    """Returns basic details about a given student (e.g. name, goals, availability, local time, progress)."""

    data = get_student_info(user_id)
    if data is None:
        return abort(404, description='Student not found')

    content = {
        "current_user": current_user,
        'student': data
    }
    
    form = SupportForm()
    return render_template('student_profile.html', form=form, title=content['student']['username'], **content)


@StudentBlueprint.route('/<user_id>/logs', methods=['GET'])
@login_required
def get_student_logs(user_id):
    """Fetches and displays the support logs for a given student."""


    student = get_student_info(user_id)

    if student is None:
        return abort(404, description='Student not found')

    support_logs = get_student_support_logs(user_id)
    form = SupportForm()


    content = {
        'current_user': current_user,
        'student': student,
        'support_logs': support_logs
    }

    return render_template('student_logs.html', form=form, title=content['student']['username'], **content)


@StudentBlueprint.route('/<user_id>/progress', methods=['GET'])
@login_required
def get_student_progress(user_id):
    """Fetches and displays course progress information for a given student."""
    # TODO: change to proper backend calls that include all the data (also from base_content!)
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


@StudentBlueprint.route('/<user_id>/notes', methods=['GET'])
@login_required
def get_student_notes(user_id):
    """Fetches and displays all mentor notes for a given student."""


    student = get_student_info(user_id)
    if student is None:
        return abort(404, description='Student not found')

    notes = get_student_notes_by_student(user_id)

    content = {
        'current_user': current_user,
        'student': student,
        'notes': notes,
    }


    form = SupportForm()
    return render_template('student_notes.html', form=form, title=content['student']['username'], **content)
