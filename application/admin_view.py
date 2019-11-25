from flask import Blueprint, jsonify, request

from . import db
from .models import User, Mentor

AdminApi = Blueprint('admin_api', __name__)

# Mentor list overview

# Assign student to mentor page
@AdminApi.route('<admin_id>', methods=['POST'])
def assign_student():
    

# Assigned students list overview

# Mentor detail page. Log of support given

# Student detail page. Log of support received

# Analytics page overview. Mentored students lists with stats

# Non-mentored student list with stats

# Assigned Students List Overview. GET all students for the mentor 
@MentorApi.route('/create', methods=['GET'])