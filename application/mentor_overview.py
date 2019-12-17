from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import requests

from . import db
from .models import User, Mentor, Student, Course, SupportLog, UserCourse

MentorOverviewBlueprint = Blueprint('mentor_overview', __name__)

# Assign a student and a mentor. Update the students table
@MentorOverviewBlueprint.route('/assign', methods=['POST', 'GET'])
def assign_student_mentor():

    # Query to show students and all their assigned mentors
    student_mentors_query = """
SELECT
  s.user_id AS student_id
 ,u.first_name||' '||u.last_name AS student_name
 ,m.user_id AS mentor_id
 ,um.first_name||' '||um.last_name AS mentor_name
FROM
  students AS s
LEFT JOIN 
  mentors AS m
ON
  m.id = s.mentor_id
LEFT JOIN
  users AS u
ON
  u.id = s.user_id
LEFT JOIN
  users AS um
ON
  um.id = m.user_id
    """
    student_mentors_proxy = db.engine.execute(text(student_mentors_query)).fetchall()

    student_mentors = jsonify([dict(row) for row in student_mentors_proxy])


    # Drop down of all students and their courses
    students_query = """
    SELECT
  s.user_id
 ,u.first_name||' '||u.last_name AS name
 ,uc.course_id
 ,c.course_name
FROM
  students AS s
INNER JOIN
  users AS u
ON
  u.id = s.user_id
LEFT JOIN
  user_courses AS uc
ON
  uc.user_id = s.user_id
LEFT JOIN
  courses AS c
ON
  c.id = uc.course_id
ORDER BY
  user_id ASC
"""
    students_proxy = db.engine.execute(text(students_query)).fetchall()
    students = jsonify([dict(row) for row in students_proxy])

    # # Drop down of all mentors and the courses
    mentors_query = """
    SELECT
  m.user_id
 ,u.first_name||' '||u.last_name AS name
 ,uc.course_id
 ,c.course_name
FROM
  mentors AS m
INNER JOIN
  users AS u
ON
  u.id = m.user_id
LEFT JOIN
  user_courses AS uc
ON
  uc.user_id = m.user_id
LEFT JOIN
  courses AS c
ON
  c.id = uc.course_id
ORDER BY
  user_id ASC
"""
    mentors_proxy = db.engine.execute(text(mentors_query)).fetchall()
    mentors = jsonify([dict(row) for row in mentors_proxy])

    # Gets the given student_id from the database
    student = Student.query.filter_by(id==request.form.student_id.data).first()

    # Assigns the mentor id to the student
    student.mentor_id = request.form.mentor_id.data
    db.session.commit()

    return mentors
    
# Gets stats for mentored and non-mentored students
@MentorOverviewBlueprint.route('/analytics', methods=['GET'])
def get_analytics():
    stats = Student.query.all()
    student_stats = [row.to_dict() for row in stats]
    return jsonify(student_stats)
