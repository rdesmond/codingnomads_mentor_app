from flask import Blueprint, jsonify, request

from . import db
from .models import User, Mentor, Student, Course, SupportLog, user_courses

Mentor = Blueprint('mentor', __name__)

# Returns details about a given mentor including name, current students / spare capacity, availability, local time, assigned students, notes, support log
@Mentor.route('/<mentor_id>', methods=['GET'])
def get_mentor(mentor_id):
    pass

# Log support for a given student
@Mentor.route('/<mentor_id>/<student_id>', methods=['POST'])
def student_log_support(student_id):
    pass
