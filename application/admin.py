from pytz import all_timezones_set
from flask import current_app as app
from flask import url_for
from flask_admin import Admin, BaseView, expose
from . import db
from .models import User, Student, Mentor, SupportLog
from flask_admin.contrib.sqla import ModelView
from .data_services import get_all_students


admin = Admin(app, name='CN Mentor Portal', template_mode='bootstrap3')


class UserView(ModelView):
    can_delete = False
    page_size = 50
    can_view_details = True
    column_searchable_list = ['first_name', 'last_name', 'email']
    column_filters = ['is_student', 'is_mentor', 'is_admin']
    create_modal = True
    edit_modal = True
    column_exclude_list = ['time_modified', 'time_created',
                           'created_at', 'updated_at',
                           'forum', 'password_hash', 'last_login', 'learning_platform', 'slack']
    form_excluded_columns = ['time_modified', 'time_created',
                             'created_at', 'updated_at',
                             'forum', 'password_hash', 'last_login', 'first_access', 'last_access']
    form_choices = {
        'timezone': [(tz, tz) for tz in all_timezones_set]
    }


class StudentView(ModelView):
    page_size = 50
    column_searchable_list = ['status', 'preferred_learning']
    column_filters = ['status', 'preferred_learning']
    create_modal = True
    edit_modal = True
    column_exclude_list = ['end_date']
    form_excluded_columns = column_exclude_list.copy()
    form_choices = {
        'status': [
            ('student', 'student'),
            ('content', 'content'),
            ('on pause', 'on pause'),
            ('alumni', 'alumni'),
            ('dropped out', 'dropped out'),
            ('lead', 'lead'),
            ('hot lead', 'hot lead'),
            ('MIA student', 'MIA student'),
            ('beta', 'beta')
        ]
    }


class MentorView(ModelView):
    page_size = 50
    column_searchable_list = ['current_students']
    column_filters = ['current_students']  # TODO: add column that shows current capacity of mentor
    create_modal = True
    edit_modal = True
    form_choices = {
        'rating': [
            (5, 5),
            (4, 4),
            (3, 3),
            (2, 2),
            (1, 1)
        ]
    }


class SupportLogView(ModelView):
    column_searchable_list = ['mentor_id', 'student_id', 'support_type']
    column_filters = ['mentor_id', 'student_id', 'comprehension', 'support_type', 'time_spent']
    create_modal = True
    edit_modal = True
    column_exclude_list = ['updated_at']
    form_excluded_columns = column_exclude_list.copy() + ['created_at']
    form_choices = {
        'support_type': [  # TODO: centralize to make sure this stays up-to-date
            ('call', 'Call'),
            ('chat', 'Chat'),
            ('meeting', 'Meeting'),
            ('forum', 'Forum'),
            ('email', 'Email')
        ],
        'comprehension': [
            (5, 'excellent'),
            (4, 'good'),
            (3, 'okay'),
            (2, 'somewhat'),
            (1, 'very little')
        ]
    }


class AnalyticsView(BaseView):
    # TODO: write the backend calls that gather and display analytics data we want
    @expose('/')
    def index(self):
        users = [
            {'user1': 'Joe'},
            {'user2': 'Billy'}
            ]
        return self.render('admin/analytics.html', users=users)


admin.add_view(UserView(User, db.session, endpoint='users'))
admin.add_view(StudentView(Student, db.session, endpoint='students'))
admin.add_view(MentorView(Mentor, db.session, endpoint='mentors'))
admin.add_view(SupportLogView(SupportLog, db.session, endpoint='logs'))
admin.add_view(AnalyticsView(name='Analytics', endpoint='analytics'))