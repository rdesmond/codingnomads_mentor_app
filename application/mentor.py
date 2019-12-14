from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select
from sqlalchemy import text

from . import db
from .models import User, Mentor, Student, Course, SupportLog, UserCourse

Mentor = Blueprint('mentor', __name__)

# Returns details about a given mentor including name, current students / spare capacity, availability, local time, assigned students, notes, support log
@Mentor.route('/<mentor_id>', methods=['GET'])
def get_mentor(mentor_id):
    # Get info from DB
    # mentor = Mentor.query.filter(Mentor.id==mentor_id).first()
    # mentor = db.session.query([Mentor]).all()
    query = """
    SELECT
      *
    FROM
      mentors
    WHERE
      id = :mentor_id
      """

    mentor = db.engine.execute(text(query), mentor_id=mentor_id)

    if mentor is None:
        return 'mentor not found', 404
    return jsonify(dict(mentor.fetchone())), 200

# Log support for a given student
@Mentor.route('/<mentor_id>/<student_id>', methods=['POST'])
def student_log_support(mentor_id, student_id):

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

