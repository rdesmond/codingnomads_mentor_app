from flask import Blueprint, request, flash, redirect, url_for
from flask_login import current_user
from application.forms import SupportForm
from application.data_services import log_student_support


ApiBlueprint = Blueprint('api', __name__)


@ApiBlueprint.route('/support', methods=['POST'])
def log_support():
    """Submits a support log."""
    # TODO: fill mentor_id from currently logged in user, and (if called from a student page) also student_id
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

        log_student_support(mentor_id,
            student_id,
            support_type,
            time_spent,
            notes,
            comprehension)
        return redirect(url_for('mentor.get_mentor', mentor_id=mentor_id))  # request.url   <- returns to current page
    else:
        flash('Missing data. Please fill all the fields')
        return redirect(url_for('overview.show_mentor_list'))
        # return redirect(url_for(request.url))  # request.url   <- returns to current page (if it works)
