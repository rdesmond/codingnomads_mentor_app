from flask import Blueprint, jsonify, request, render_template
from . import db
from .models import User, Mentor, Student, Course, SupportLog, UserCourse
from .forms import SupportForm

StudentOverviewBlueprint = Blueprint('student_overview', __name__)


# Returns students for a given mentor and some stats (time since last login, course completion percentage, time since last contact)
@StudentOverviewBlueprint.route('/<mentor_id>', methods=['GET'])
def get_student_overview(mentor_id):
    query = """
SELECT
  s.user_id
 ,uc.course_id
 ,c.course_name
FROM
  students AS s
LEFT JOIN
  user_courses AS uc
ON
  uc.user_id = s.user_id
LEFT JOIN
  courses AS c
ON
  c.id = uc.course_id
"""
    result_proxy = db.engine.execute(text(query)).fetchall()
    student_overview = jsonify([dict(row) for row in result_proxy])

    if student_overview is None:
        return 'not found', 404
    return student_overview, 200


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

    support_log = SupportLog(
        mentor_id=mentor_id, student_id=student_id, support_type=support_type,
         time_spent=time_spent, notes=notes, mentor_assesment=mentor_assesment)
    db.session.add(support_log)
    db.session.commit()
    return "Success"

# View Logs for a given student
@StudentOverviewBlueprint.route('/logs/<mentor_id>/<student_id>', methods=['GET'])
def view_support_log(mentor_id, student_id):
    logs = SupportLog.query.filter(SupportLog.mentor_id == mentor_id).filter(SupportLog.student_id == student_id).all()
    if logs is None:
        return 'not found', 404
    else:
        formatted_logs = [log.to_dict() for log in logs]

    return render_template('log_list.html', logs=formatted_logs, student_id=student_id)  # TODO: feels weird to always pass this form
    #return jsonify(formatted_logs), 200

# TODO: how to write DRY flask routes and forms
