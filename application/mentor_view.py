from flask import Blueprint, jsonify, request

from . import db
from .models import User, Mentor, Student

Mentor = Blueprint('mentor', __name__)

# Assigned Students List Overview. GET all students for the mentor
@Mentor.route('/<mentor_id>/students', methods=['GET'])
def get_mentor_students(mentor_id):
    students = Student.query.filter(Student.mentor_id == mentor_id )

    if student is None:
        return "Mentor has no students"
    
    return jsonify([student.from_dict() for student in students])

@Mentor.route('/<student_id>', methods=['GET'])
# Student Detail Page. GET from support logs
def get_student_details(student_id):
    pass

# Mentor Detail Page. GET from mentors
@Mentor.route('/<mentor_id>', methods=['GET'])
def get_mentor_details(mentor_id):
    pass

# Log support modal. GET.
@Mentor.route('/<mentor_id>/support', methods=['GET'])
def get_support(mentor_id):
    pass

# Log support modal. POST.
@Mentor.route('/<mentor_id>/support', methods=['POST'])
def post_support(mentor_id):
    pass

