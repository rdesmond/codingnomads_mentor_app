from flask import Blueprint, jsonify, request

from . import db
from .models import User, Mentor, Student, Course, SupportLog, UserCourse

from .utils import utc_to_local

Student = Blueprint('student', __name__)

# Returns details about a given student including name ,goals, availability, local time, progress, notes and support log
@Student.route('/<student_id>', methods=['GET'])
def get_student(student_id):

    # Dummy data

    data = {

    }

    return "test message"


# Log support for a given student
@Student.route('/support/<student_id>', methods=['POST'])
def log_support_student(student_id):
    pass


