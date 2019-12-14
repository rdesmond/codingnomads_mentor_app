from flask import Blueprint, jsonify, request

from . import db
from .models import User, Mentor, Student, Course, SupportLog, UserCourse

from .utils import utc_to_local

StudentBlueprint = Blueprint('student', __name__)

# Returns details about a given student including name ,goals, availability, local time, progress, notes and support log
@StudentBlueprint.route('/<student_id>', methods=['GET'])
def get_student(student_id):

    # Get info from DB
    student = Student.query.filter(Student.id==student_id).first()

    if student is None:
        return 'student not found', 404
    return jsonify(student.to_dict()), 200


# Log support for a given student
@StudentBlueprint.route('/support/<student_id>', methods=['POST'])
def log_support_student(student_id):

    # Create a row in the support log table
    mentor_id = request.form['mentor_id']
    support_type = request.form['support_type']
    time_spent = request.form['support_type']
    notes = request.form['notes']
    mentor_assesment = request.form['mentor_assesment']


    support_log = SupportLog(
        mentor_id=mentor_id, student_id=student_id, support_type=support_type,
        time_spent=time_spent, notes=notes, mentor_assesment=mentor_assesment)
    db.session.add(support_log)
    db.session.commit()
    return "Success"


