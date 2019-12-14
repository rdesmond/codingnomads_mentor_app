from flask import Blueprint, jsonify, request, render_template
from . import db
from .models import User, Mentor, Student, Course, SupportLog, UserCourse
from .forms import SupportForm

StudentOverview = Blueprint('student_overview', __name__)


# Returns students for a given mentor and some stats (time since last login, course completion percentage, time since last contact)
@StudentOverview.route('/<mentor_id>', methods=['GET'])
def get_student_overview(mentor_id):
    # TODO: what were you trying to do here? currently not working. why the join?
    student_overview = UserCourse.query.join(Student).filter(Student.mentor_id == mentor_id)

    if student_overview is None:
        return 'not found', 404
    return jsonify(student_overview.to_dict()), 200


# Log support for a given student
@StudentOverview.route('/<mentor_id>/support/<student_id>', methods=['POST'])
def log_support(mentor_id, student_id):
    # dummy data
    data = {
        'mentor_id': '1',
        'student_id': '2',
        'support_type': 'call',
        'created_at': '2019-11-28 00:00:00',
        'time_spent': '30',
        'notes': 'Some test notes',
        'mentor_assesment': '5'
    }

    input = SupportLog.from_dict(data)
    db.session.add(input)
    db.session.commit()


# View Logs for a given student
@StudentOverview.route('/logs/<mentor_id>/<student_id>', methods=['GET'])
def view_support_log(mentor_id, student_id):
    logs = SupportLog.query.filter(SupportLog.mentor_id == mentor_id).filter(SupportLog.student_id == student_id).all()
    if logs is None:
        return 'not found', 404
    else:
        formatted_logs = [log.to_dict() for log in logs]

    return render_template('log_list.html', logs=formatted_logs, student_id=student_id)  # TODO: feels weird to always pass this form
    #return jsonify(formatted_logs), 200

# TODO: how to write DRY flask routes and forms
