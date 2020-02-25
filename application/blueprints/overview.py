import json
from flask import Blueprint, jsonify, request, abort, render_template
from flask_login import current_user, login_required
from application.forms import SupportForm
from application.data_services import get_all_students, get_mentors_and_students, get_students_with_courses, get_all_student_info
from application.data_services import get_mentors_with_courses, assign_students_to_mentor, get_all_mentor_info


OverviewBlueprint = Blueprint('overview', __name__)


# Assign a student and a mentor. Update the students table
@OverviewBlueprint.route('/assign', methods=['POST', 'GET'])
@login_required
def assign_student_mentor():
    # Query to show students and all their assigned mentors
    student_mentor_data = jsonify(get_mentors_and_students())
    # Drop down of all students and their courses
    students = jsonify(get_students_with_courses())
    # Drop down of all mentors and the courses
    mentors = jsonify(get_mentors_with_courses())
    # Assigns the mentor id to the student
    student_id = request.form.student_id.data
    mentor_id = request.form.mentor_id.data
    assign_students_to_mentor(student_id, mentor_id)
    return mentors


# Gets stats for mentored and non-mentored students
@OverviewBlueprint.route('/analytics', methods=['GET'])
@login_required
def get_analytics():
    data = get_all_students()
    if not data:
        return abort(404, description='Students not found')
    return jsonify(data)


# TODO: change this to actual backend call
@OverviewBlueprint.route('/mentors', methods=['GET'])
@login_required
def show_mentor_list():
    form = SupportForm()

    mentors = get_all_mentor_info()

    # TODO replace hard coded value with real query
    for mentor in mentors:
        mentor['last_support_log_created'] = "2020-01-01 11:19:06.782213"



    content = {
        'mentors': mentors,
        'current_user': current_user
    }

    return render_template('mentor_overview.html', form=form, title='Mentors', **content)


# TODO: change this to actual backend call
@OverviewBlueprint.route('/students', methods=['GET'])
@login_required
def show_student_list():


    mentors_list = []
    mentors = get_all_mentor_info()
    for mentor in mentors:
        mentors_list.append({
            "mentor_id": mentor['id'],
            "name": mentor['first_name']
        })

    

    students = get_all_student_info()
    content = {
        'current_user': current_user,
        'students': students,
        'mentors': mentors_list,
    }


    form = SupportForm()
    return render_template('student_overview.html', form=form, title='Students', **content)
