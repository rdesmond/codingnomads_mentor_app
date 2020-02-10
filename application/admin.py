from pytz import all_timezones_set
from flask import current_app as app
from flask import url_for, redirect
from flask_admin import Admin, BaseView, expose
from . import db
from .models import User, Student, Mentor, SupportLog
from flask_admin.contrib.sqla import ModelView
from .data_services import get_all_students
from flask_login import current_user


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

    def is_accessible(self):
        
        if current_user.is_authenticated and current_user.is_admin == True:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))


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

    def is_accessible(self):
        
        if current_user.is_authenticated and current_user.is_admin == True:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))


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

    def is_accessible(self):
        
        if current_user.is_authenticated and current_user.is_admin == True:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))


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

    def is_accessible(self):
        
        if current_user.is_authenticated and current_user.is_admin == True:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))

class AnalyticsView(BaseView):
    # TODO: write the backend calls that gather and display analytics data we want
    @expose('/')
    def index(self):
        """ REQUIREMENTS:
        - How much time did one mentor spend on support in a given time frame?
        - How much of that time went to which type of support?
        - How much of that time went to which student?
        - What is the feedback that a mentor receives from their students?
        - The student Overview page shows a note of how much time of mentorship a student has received per week
        """
        example_json = [
            {
                "mentor_id": 1,
                "mentor_firstname": "Gilad",
                "mentor_lastname": "Gressel",
                "support_type_times_total": {
                    "call": 100,
                    "chat": 100,
                    "talk": 100,
                    "email": 50,
                    "total": 350
                },
                "mentor_rating_total": 4.7,
                "student_support_times": [
                    {
                        "student_id": 2,
                        "student_firstname": "Johnny",
                        "student_lastname": "Appleseed",
                        "support_type_times": {
                            "call": 50,
                            "chat": 50,
                            "talk": 50,
                            "email": 0,
                            "total": 150
                        },
                        "mentor_rating": 4
                    },
                    {
                        "student_id": 3,
                        "student_firstname": "Carol",
                        "student_lastname": "Dweck",
                        "support_type_times": {
                            "call": 50,
                            "chat": 50,
                            "talk": 50,
                            "email": 50,
                            "total": 200
                        },
                        "mentor_rating": 5
                    }
                ]
            }
        ]
        return self.render('admin/analytics.html', data=example_json)


    def is_accessible(self):
        
        if current_user.is_authenticated and current_user.is_admin == True:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))


class LeadView(BaseView):
    # TODO: write the backend calls that gather and display analytics data we want
    @expose('/')
    def index(self):
        """ REQUIREMENTS:
        - When has a student last logged in?
        - What resources have they completed?
        - When did they decide to purchase (if so)?
        - What frequency is their interaction with the learning platform?
        - Did they recently stop interacting? Where? When?
        """
        leads_json = [
            {
                "last_access": "2020-01-19",
                "completed_resources": [
                    "Python Intro",
                    "Python Outro"
                ],
                "purchase_info": {
                    "purchased": True,
                    "timestamp": "2019-12-31",
                    "resource": "Python Outro"
                },
                "interactions": [

                ]
            }
        ]
        return self.render('admin/leads.html', data=leads_json)

    def is_accessible(self):
        
        if current_user.is_authenticated and current_user.is_admin == True:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))

admin.add_view(UserView(User, db.session, endpoint='users'))
admin.add_view(StudentView(Student, db.session, endpoint='students'))
admin.add_view(MentorView(Mentor, db.session, endpoint='mentors'))
admin.add_view(SupportLogView(SupportLog, db.session, endpoint='logs'))
admin.add_view(AnalyticsView(name='Analytics', endpoint='analytics'))
admin.add_view(LeadView(name='Leads', endpoint='leads'))
