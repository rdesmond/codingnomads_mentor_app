from flask import Blueprint, jsonify, request, render_template, flash, redirect
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
# TODO: maybe this shouldn't be its own URL? could be a JS function through the pop-up
@StudentBlueprint.route('/support/<student_id>', methods=['POST'])
def log_support_student(student_id):

    form = SupportForm()
    if form.validate_on_submit():
        flash('Support log submitted for student #{} by mentor #{}'.format(
            form.mentor_id.data, form.student_id.data))
        return redirect(url_for('index'))

    # Create a row in the support log table
    mentor_id = request.form['mentor_id']  # TODO: this should come from the authenticated_user
    support_type = request.form['support_type']
    time_spent = request.form['time_spent']
    notes = request.form['notes']
    comprehension = request.form['comprehension']  # TODO: update name. this is about how well the student is doing


    support_log = SupportLog(
        mentor_id=mentor_id, student_id=student_id, support_type=support_type,
        time_spent=time_spent, notes=notes, comprehension=comprehension)
    db.session.add(support_log)
    db.session.commit()
    return "Success"


