from flask import Blueprint, jsonify, request

from . import db
from .models import User, Mentor

AdminApi = Blueprint('admin_api', __name__)

# Mentor list overview

# Assign student to mentor page
@AdminApi.route()
def assign_student():
    user_id = str(current_user.get_id())
    messagetext = request.json["content"]

    try:
        newmessage = Message.from_messages(messagetext, chat_id, user_id)
    except KeyError as e:
        return jsonify(f'Missing key: {e.args[0]}'), 400

    db.session.add(newmessage)
    db.session.commit()
    return jsonify(newmessage.to_messages()), 200
# Assigned students list overview

# Mentor detail page. Log of support given

# Student detail page. Log of support received

# Analytics page overview. Mentored students lists with stats

# Non-mentored student list with stats

# Assigned Students List Overview. GET all students for the mentor 
@MentorApi.route('/create', methods=['GET'])