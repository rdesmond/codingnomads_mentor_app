from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests

from . import db
from .models import User, Mentor, Student, Course, SupportLog, UserCourse

MentorOverview = Blueprint('mentor_overview', __name__)

# Assign a student and a mentor. Update the students table
@MentorOverview.route('/assign', methods=['POST', 'GET'])
def assign_student_mentor():

    # Query to show students and all their assigned mentors
    student_mentors_query =
    """
    SELECT
      s.id AS student_id
     ,us.first_name AS student_first_name
     ,us.last_name AS student_last_name
     ,s.mentor_id
     ,um.first_name AS mentor_first_name
     ,um.last_name AS mentor_last_name
    FROM
      students AS s
    LEFT JOIN
      users AS us
    ON
      us.id = s.user_id
    LEFT JOIN
      users AS um
    ON
      um.id = s.mentor_id
    """
    student_mentors_proxy = db.engine.execute(text(student_mentors_query).execution_options(autocommit=True)) 


    # Drop down of all students and their courses
    students = Student.query.join(UserCourse).join(Course.id==UserCourse.course_id).join(User.id==Student.user_id)
    students = [row.to_dict() for row in students]


    # Drop down of all mentors and the courses
    mentors = Mentor.query.join(UserCourse).join(Course.id==UserCourse.course_id),join(User.id==Mentor.user_id)
    mentors = [row.to_dict for row in mentors]

    # Gets the given student_id from the database
    student = Student.query.filter_by(id==request.form.student_id.data).first()

    # Assigns the mentor id to the student
    student.mentor_id = request.form.mentor_id.data
    db.session.commit()

# Gets stats for mentored and non-mentored students
@MentorOverview.route('/analytics', methods=['GET'])
def get_analytics():
    stats = Student.query
    student_stats = [row.to_dict() for row in stats]
    return jsonify(student_stats)
