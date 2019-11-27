from flask import Blueprint, jsonify, request

from . import db
from .models import User, Mentor

Admin = Blueprint('admin', __name__)

# Assigned students list overview. GET from student_mentors
@Admin.route('/students', methods=['GET'])
def get_student_mentors(admin_id):
    pass

# Assign mentors and students. POST to student_mentors
@Admin.route('/students', methods=['POST'])
def assign_student_mentors(admin_id):
    pass

# Mentor detail page. GET from support_logs
@Admin.route('/mentors/<mentor_id>', methods=['GET'])
def get_mentor_details(admin_id, mentor_id):
    pass

# Student detail page. GET from support_logs
@Admin.route('/students/<student_id>', methods=['GET'])
def get_student_details(admin_id, student_id):
    pass

# Mentored list stats.  API request / GET request from students table.
@Admin.route('/analytics/mentored', methods=['GET'])
def get_student_stats(admin_id):
    pass

# Non-mentored student list stats. API request / GET request from students table.
@Admin.route('/analytics/non-mentored', methods=['GET'])
def get_non_student_stats(admin_id):
    pass


