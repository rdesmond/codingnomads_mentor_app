from flask import Blueprint, jsonify, request

from . import db
from .models import User, Mentor, Student, Course, SupportLog, UserCourse

MentorOverview = Blueprint('mentor_overview', __name__)

# Assign a student and a mentor. Update the students table
@MentorOverview.route('/assign', methods=['POST'])
def assign_student_mentor():
    student = Student.query.filter_by(id==form.student_id.data).first()
    student.mentor_id = form.mentor_id.data
    db.session.commit()

# Gets stats for mentored and non-mentored students
@MentorOverview.route('/analytics', methods=['GET'])
def get_analytics():
    response = requests.get('URL')
