from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
from .utils import utc_to_local
from . import db
from .models import User, Mentor, Student, Course, SupportLog, UserCourse
from .forms import SupportForm

StudentBlueprint = Blueprint('student', __name__)

# Returns details about a given student including name ,goals, availability, local time, progress, notes and support log
@StudentBlueprint.route('/<student_id>', methods=['GET'])
def get_student(student_id):

    # Get info from DB
    student = Student.query.filter(Student.id==student_id).first()

    if student is None:
        return 'student not found', 404
    return jsonify(student.to_dict()), 200


# Log support for a given student
@StudentBlueprint.route('/support/<student_id>', methods=['POST'])
def log_support_student(student_id):  # TODO: input could be mentor_id from currently logged in user (+add below)

    form = SupportForm()
    if form.validate_on_submit():
        flash('Support Log submitted for student #{} by mentor #{}'.format(
            form.mentor_id.data, form.student_id.data))

        # Create a row in the support log table
        mentor_id = request.form['mentor_id']  # TODO: this should come from the authenticated_user
        student_id = request.form['student_id']
        support_type = request.form['support_type']
        time_spent = request.form['time_spent']
        notes = request.form['notes']
        comprehension = request.form['comprehension']

        support_log = SupportLog(
            mentor_id=mentor_id, student_id=student_id, support_type=support_type,
            time_spent=time_spent, notes=notes, comprehension=comprehension)
        db.session.add(support_log)
        db.session.commit()
    else:
        flash('Missing data. Please fill all the fields')
    return redirect(url_for('index'))


