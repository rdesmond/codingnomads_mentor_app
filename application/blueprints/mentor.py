import json
from flask import Blueprint, jsonify, request, abort, render_template
from flask_login import current_user, login_required
from application.data_services import get_mentor_info, log_student_support, get_mentor_info_with_students
from application.forms import SupportForm


MentorBlueprint = Blueprint('mentor', __name__)

# TODO: remove base_content once DB calls are set up properly
base_content = json.loads("""{
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
base_content['current_user'] = current_user


@MentorBlueprint.route('/<user_id>', methods=['GET'])
@login_required
def get_mentor(user_id):
    """Returns base details about a mentor (e.g. name, current students / spare capacity, availability, local time)."""
    # Get info from DB

    data = get_mentor_info(user_id)

    if data is None:
        return abort(404, 'Mentor not found')

    content = {
        "current_user": current_user,
        "mentor": data
    }
    form = SupportForm()
    return render_template('mentor_profile.html', form=form, title=content['mentor']['username'], **content)


@MentorBlueprint.route('/<user_id>/students', methods=['GET'])
@login_required
def get_mentored_students(user_id):
    """Get list of students currently assigned to given mentor."""
    # TODO: handel next_call object in the student info

    data = get_mentor_info_with_students(user_id)

    if data is None:
        return abort(404, 'Mentor not found')

    content = {
        "current_user": current_user,
        "mentor": data,
    }

    form = SupportForm()
    return render_template('mentor_students.html', form=form, title=content['mentor']['username'], **content)



@MentorBlueprint.route('/<mentor_id>/notes', methods=['GET'])
@login_required
def get_mentor_notes(mentor_id):
    """Get all notes written by given mentor."""
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


@MentorBlueprint.route('/<mentor_id>/logs', methods=['GET'])
@login_required
def get_mentor_logs(mentor_id):
    """Get all support logs written by given mentor."""
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
            "student_id": 2,
            "notes": "call went well, we discussed exceptions.",
            "created_at": "Fri, 23 Sep 2019 13:14:57 GMT",
            "support_type": "call",
            "time_spent": 30,
            "comprehension": 5
        }
    ]
}"""))
    return render_template('mentor_logs.html', form=form, title=content['mentor']['username'], **content)
