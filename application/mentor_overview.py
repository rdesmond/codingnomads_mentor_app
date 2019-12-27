from flask import Blueprint, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import requests

from . import db
from .models import User, Mentor, Student, Course, SupportLog, UserCourse
from .data_services import get_all_students, get_mentors_and_students, get_students_with_courses, get_mentors_with_courses, get_student_info, assign_students_to_mentor

MentorOverviewBlueprint = Blueprint('mentor_overview', __name__)

# Assign a student and a mentor. Update the students table
@MentorOverviewBlueprint.route('/assign', methods=['POST', 'GET'])
def assign_student_mentor():

    # Query to show students and all their assigned mentors

    student_mentor_data = jsonify(get_mentors_and_students())


    # Drop down of all students and their courses
    
    students = jsonify(get_students_with_courses())

    # # Drop down of all mentors and the courses

    mentors = jsonify(get_mentors_with_courses())

    # Assigns the mentor id to the student

    student_id = request.form.student_id.data
    mentor_id = request.form.mentor_id.data
    
    assign_students_to_mentor(student_id, mentor_id)

    return mentors
    
# Gets stats for mentored and non-mentored students
@MentorOverviewBlueprint.route('/analytics', methods=['GET'])
def get_analytics():

  data = get_all_students()

  if not data:
    return abort(404, description='Students not found')
  
  return jsonify(data)