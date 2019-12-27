from flask import Blueprint, jsonify, request, render_template, abort
from application import db
from application.models import User, Mentor, Student, Course, SupportLog, UserCourse
from application.forms import SupportForm
from application.data_services import get_student_overview, log_student_support, get_student_support_logs

StudentOverviewBlueprint = Blueprint('student_overview', __name__)


# Returns students for a given mentor and some stats (time since last login, course completion percentage, time since last contact)
@StudentOverviewBlueprint.route('/<mentor_id>', methods=['GET'])
def student_overview(mentor_id):

    data = get_student_overview(mentor_id)

    if data is None:
        return abort(404, description='Mentor not found')
    return jsonify(data), 200


# Log support for a given student
@StudentOverviewBlueprint.route('/<mentor_id>/support/<student_id>', methods=['POST'])
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

    # # Code for when a form is built on the front end
    # mentor_id = request.form['mentor_id']
    # support_type = request.form['support_type']
    # time_spent = request.form['support_type']
    # notes = request.form['notes']
    # mentor_assesment = request.form['mentor_assesment']

    mentor_id = mentor_id
    student_id = student_id
    support_type = 'test'
    time_spent = 5
    notes ='test'
    mentor_assesment = 5

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

# View Logs for a given student
@StudentOverviewBlueprint.route('/logs/<mentor_id>/<student_id>', methods=['GET'])
def view_support_log(mentor_id, student_id):

    data = get_student_support_logs(mentor_id, student_id)

    if data is None:
        return abort(404, description='Student or mentor not found')

    return render_template('log_list.html', logs=data, student_id=student_id)  # TODO: feels weird to always pass this form
    #return jsonify(formatted_logs), 200

# TODO: how to write DRY flask routes and forms
