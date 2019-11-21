from flask import Blueprint, jsonify, request

from . import db
from .models import User, Mentor

MentorApi = Blueprint('mentor_api', __name__)

# Gets all mentors and student
@MentorApi.route('/create', methods=['GET'])
def get_mentor_students():
    pass

