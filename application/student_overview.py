from flask import Blueprint, jsonify, request

from . import db
from .models import User, Mentor, Student, Course, SupportLog, user_courses

StudentOverview = Blueprint('student_overview', __name__)

# Returns students for a given mentor and some stats (time since last login, course completion percentage, time since last contact)
@StudentOverview.route('/<mentor_id>', methods=['GET'])
def get_student_overview(mentor_id):
    # dummy data
    student_overview = user_courses.query.join(Student).filter(Student.mentor_id==mentor_id)

 

# Log support for a given student
@StudentOverview.route('/<mentor_id>/support/<student_id>', methods=['POST'])
def log_support(mentor_id, student_id):

    # dummy data
    data = {
        'mentor_id': '1',
        'student_id': '2'
        'support_type': 'call',
        'created_at': '2019-11-28 00:00:00',
        'time_spent': '30',
        'notes': 'Some test notes',
        'mentor_assesment': '5'
    }

    input = SupportLog.from_dict(data)
    db.session.add(input)
    db.session.commit()





