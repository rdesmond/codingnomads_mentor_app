from flask import Blueprint, jsonify, request

from . import db
from .models import User, Mentor, Student, Course, SupportLog, UserCourse

MentorOverview = Blueprint('mentor_overview', __name__)

# Assign a student and a mentor. Insert into student_mentors.
@MentorOverview.route('/assign', methods=['POST'])
def assign_student_mentor():
    pass


# Gets stats for mentored and non-mentored students
@MentorOverview.route('/analytics', methods=['GET'])
def get_analytics():
    pass