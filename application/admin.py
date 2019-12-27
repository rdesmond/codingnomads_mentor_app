from flask import current_app as app
from flask_admin import Admin, BaseView, expose
from . import db
from .models import User, Student, Mentor, SupportLog
from flask_admin.contrib.sqla import ModelView


admin = Admin(app, name='CodingNomads Mentor App', template_mode='bootstrap3')


class UserView(ModelView):
    # TODO: customize user views in admin panel
    pass


class AnalyticsView(BaseView):
    @expose('/')
    def index(self):
        return 'Hello World'

admin.add_view(ModelView(User, db.session, endpoint='user_admin'))
admin.add_view(ModelView(Student, db.session, endpoint='student_admin'))
admin.add_view(ModelView(Mentor, db.session, endpoint='mentor_admin'))
admin.add_view(ModelView(SupportLog, db.session, endpoint='support_log_admin'))
admin.add_view(AnalyticsView(name='Analytics', endpoint='analytics'))