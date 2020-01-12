import json
from flask import Blueprint, jsonify, request, abort, render_template
from application.forms import SupportForm
from application.data_services import get_all_students, get_mentors_and_students, get_students_with_courses, get_mentors_with_courses, get_student_info, assign_students_to_mentor


OverviewBlueprint = Blueprint('overview', __name__)

# Assign a student and a mentor. Update the students table
@OverviewBlueprint.route('/assign', methods=['POST', 'GET'])
def assign_student_mentor():
    # Query to show students and all their assigned mentors
    student_mentor_data = jsonify(get_mentors_and_students())
    # Drop down of all students and their courses
    students = jsonify(get_students_with_courses())
    # Drop down of all mentors and the courses
    mentors = jsonify(get_mentors_with_courses())
    # Assigns the mentor id to the student
    student_id = request.form.student_id.data
    mentor_id = request.form.mentor_id.data
    assign_students_to_mentor(student_id, mentor_id)
    return mentors


# Gets stats for mentored and non-mentored students
@OverviewBlueprint.route('/analytics', methods=['GET'])
def get_analytics():
    data = get_all_students()
    if not data:
        return abort(404, description='Students not found')
    return jsonify(data)


# TODO: change this to actual backend call
@OverviewBlueprint.route('/mentors', methods=['GET'])
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
@OverviewBlueprint.route('/students', methods=['GET'])
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
            "last_name": "Dunlop",
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
    ],
    "mentors": [
        { "mentor_id":  1, "name":  "Ryan"},
        { "mentor_id":  2, "name":  "Martin"},
        { "mentor_id":  3, "name":  "Gilad"}
    ]
}
""")
    return render_template('student_overview.html', form=form, title='Students', **content)
