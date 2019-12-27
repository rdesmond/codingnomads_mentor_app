from flask import Blueprint, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select
from sqlalchemy import text

from . import db
from .models import User, Mentor, Student, Course, SupportLog, UserCourse
from .data_services import get_mentor_info, log_student_support

MentorBlueprint = Blueprint('mentor', __name__)


# Returns details about a given mentor including name, current students / spare capacity, availability, local time, assigned students, notes, support log
@MentorBlueprint.route('/<mentor_id>', methods=['GET'])
def get_mentor(mentor_id):

    # Get info from DB
    data = get_mentor_info(mentor_id)

    if data is None:
        return abort(404, 'Mentor not found')
    return jsonify(data), 200


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

