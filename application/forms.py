from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class SupportForm(FlaskForm):
    mentor_id = IntegerField('Mentor ID', validators=[DataRequired(message="Your mentor ID")])
    student_id = IntegerField('Student ID', validators=[DataRequired(message="ID of the student you're logging support for")])
    support_type = SelectField('Support Type',
                               choices=[('call', 'call'), ('chat', 'chat'), ('orga', 'orga'), ('forum', 'forum')],
                               validators=[DataRequired(message="How did you interact with the student")])
    time_spent = IntegerField('Time Spent', validators=[DataRequired(message="Needs to be a number")])
    notes = TextAreaField('Notes', validators=[DataRequired(message="Quickly describe the interaction")])
    comprehension = SelectField('Comprehension',
                                choices=[(5, 'excellent'), (4, 'good'), (3, 'okay'), (2, 'somewhat'), (1, 'very little')],
                                coerce=int,
                                validators=[DataRequired(message="How well did the student understand (1-5)")])
    submit = SubmitField('Submit')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    repeat_new_password = PasswordField('Repeat New Password', validators=[DataRequired(), EqualTo('New Password')])
    submit = SubmitField('Change Password')
