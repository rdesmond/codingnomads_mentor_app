from flask import Blueprint, jsonify, request

from . import db
from .models import User, Mentor, Student

MentorApi = Blueprint('mentor_api', __name__)

# Assigned Students List Overview. GET all students for the mentor
@MentorApi.route('/<mentor_id>', methods=['GET'])
def get_mentor_students(mentor_id):
    # M
    students = Student.query.filter(Student.mentor_id == mentor_id )

    if student is None:
        return "Mentor has no students"
    
    return jsonify([student.from_dict() for student in students])

# Student Detail Page
# @MentorApi.route('')

# Personal Profile Page

# Log Support page/modal


