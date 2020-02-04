from flask import Blueprint, request, flash, redirect, url_for
from flask_login import current_user, login_required
from application.forms import SupportForm
from application.data_services import log_student_support


ApiBlueprint = Blueprint('api', __name__)


@ApiBlueprint.route('/support', methods=['POST'])
@login_required
def log_support():
    """Submits a support log."""
    # TODO: (if called from a student page) automatically fill in student_id
    form = SupportForm()
    if form.validate_on_submit():
        flash('Support Log submitted for student #{} by mentor #{}'.format(
            current_user.id, form.student_id.data))

        log = {
            'mentor_id': current_user.id,
            'student_id': request.form['student_id'],
            'support_type': request.form['support_type'],
            'time_spent': request.form['time_spent'],
            'notes': request.form['notes'],
            'comprehension': request.form['comprehension'],
        }

        log_student_support(log)


        return redirect(url_for('mentor.get_mentor', user_id=current_user.id))  # request.url   <- returns to current page
    else:
        flash('Missing data. Please fill all the fields')
        # TODO: return to page it was issued from instead
        return redirect(url_for('overview.show_mentor_list'))
        # return redirect(url_for(request.url))  # request.url   <- returns to current page (if it works)
