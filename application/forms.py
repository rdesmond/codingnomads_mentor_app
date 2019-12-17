from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SupportForm(FlaskForm):
    mentor_id = IntegerField('Mentor ID', validators=[DataRequired()])
    student_id = IntegerField('Student ID', validators=[DataRequired()])
    support_type = StringField('Support Type', validators=[DataRequired()])
    time_spent = IntegerField('Time Spent', validators=[DataRequired()])
    notes = StringField('Notes', validators=[DataRequired()])
    comprehension = IntegerField('Comprehension', validators=[DataRequired()])
    submit = SubmitField('Submit')