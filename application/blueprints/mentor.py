import json
from flask import Blueprint, jsonify, request, abort, render_template
from application.data_services import get_mentor_info, log_student_support
from application.forms import SupportForm


MentorBlueprint = Blueprint('mentor', __name__)

# TODO: remove base_content once DB calls are set up properly
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


@MentorBlueprint.route('/<mentor_id>', methods=['GET'])
def get_mentor(mentor_id):
    """Returns base details about a mentor (e.g. name, current students / spare capacity, availability, local time)."""
    # Get info from DB
    data = get_mentor_info(mentor_id)
    if data is None:
        return abort(404, 'Mentor not found')

    # TODO: change to proper backend calls
    form = SupportForm()
    content = base_content
    return render_template('mentor_profile.html', form=form, title=content['mentor']['username'], **content)
    # return jsonify(data), 200


@MentorBlueprint.route('/<mentor_id>/students', methods=['GET'])
def get_mentored_students(mentor_id):
    """Get list of students currently assigned to given mentor."""
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
