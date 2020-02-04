import json
from flask import Blueprint, jsonify, request, abort, render_template
from flask_login import current_user, login_required
from application.data_services import get_mentor_info, log_student_support, get_mentor_info_with_students, get_student_notes_by_mentor, get_support_logs_by_mentor
from application.forms import SupportForm


MentorBlueprint = Blueprint('mentor', __name__)


@MentorBlueprint.route('/<user_id>', methods=['GET'])
@login_required
def get_mentor(user_id):
    """Returns base details about a mentor (e.g. name, current students / spare capacity, availability, local time)."""
    # Get info from DB

    data = get_mentor_info(user_id)

    if data is None:
        return abort(404, 'Mentor not found')

    content = {
        "current_user": current_user,
        "mentor": data
    }

    form = SupportForm()
    return render_template('mentor_profile.html', form=form, title=content['mentor']['username'], **content)


@MentorBlueprint.route('/<user_id>/students', methods=['GET'])
@login_required
def get_mentored_students(user_id):
    """Get list of students currently assigned to given mentor."""
    # TODO: handle next_call object in the student info

    data = get_mentor_info_with_students(user_id)

    if data is None:
        return abort(404, 'Mentor not found')

    content = {
        "current_user": current_user,
        "mentor": data,
    }

    form = SupportForm()
    return render_template('mentor_students.html', form=form, title=content['mentor']['username'], **content)


@MentorBlueprint.route('/<user_id>/notes', methods=['GET'])
@login_required
def get_mentor_notes(user_id):
    """Get all notes written by given mentor."""

    data = get_mentor_info(user_id)

    if data is None:
        return abort(404, 'Mentor not found')
    
    data['notes'] = get_student_notes_by_mentor(user_id)

    content = {
        'current_user': current_user,
        'mentor': data
    }

    form = SupportForm()
    return render_template('mentor_notes.html', form=form, title=content['mentor']['username'], **content)


@MentorBlueprint.route('/<user_id>/logs', methods=['GET'])
@login_required
def get_mentor_logs(user_id):
    """Get all support logs written by given mentor."""
    # TODO: change to proper backend calls

    data = get_mentor_info(user_id)

    if data is None:
        return abort(404, 'Mentor not found')

    data['support_logs'] = get_support_logs_by_mentor(user_id)


    content = {
        'current_user': current_user,
        'mentor': data
    }

    form = SupportForm()
    return render_template('mentor_logs.html', form=form, title=content['mentor']['username'], **content)
