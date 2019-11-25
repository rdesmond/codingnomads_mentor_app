from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import Column, DateTime, event, CheckConstraint
from sqlalchemy.sql import func

class User(db.Model):
    """
    Data model for users (students and mentors)
    """
    __tablename__ = 'users'

    # Adding a constraint for the role column
    __table_args__ = (CheckConstraint("role::text = ANY (ARRAY['student'::character varying, 'mentor'::character varying]::text[])", name="check_roles"),)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=func.utcnow())
    updated_at = db.Column(db.DateTime, default=func.utcnow(), onupdate=func.utcnow())
    telephone = db.Column(db.String(128))
    learning_platform = db.Column(db.String(128))
    forum = db.Column(db.String(128))
    slack = db.Column(db.String(128))
    timezone = db.Column(db.String(128))
    bio = db.Column(db.String(500))
    role = db.Column(db.String(500), default='student')


    # 1-1 relationship between users and mentors
    mentor = db.relationship('Mentor', uselist=False, back_populates='users')

    # 1-1 relationship between users and students
    student = db.relationship('Student', uselist=False, back_populates='users')

    # Many to many relationship between users and courses
    user_courses = db.relationship('Course', secondary='user_courses', backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User {}>'.format(self.username)    
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def from_dict(dict):
        return User(
               id = dict['id'], 
               username = dict['username'],
               email = dict['email'],
               password_hash = dict['password_hash'],
               first_name = dict['first_name'],
               last_name = dict['last_name'],
               created_at = dict['created_at'],
               updated_at = dict['updated_at'],
               telephone = dict['telephone'],
               learning_platform = dict['learning_platform'],
               forum = dict['forum'],
               slack = dict['slack'],
               timezone = dict['timezone'],
               bio = dict['bio'],
               role = dict['role']
        )
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'telephone': self.telephone,
            'learning_platform': self.learning_platform,
            'forum': self.forum,
            'slack': self.slack,
            'timezone': self.timezone,
            'bio': self.bio,
            'role': self.role
        }

class Mentor(db.Model):

    """
    Data model for mentors
    """

    __tablename__ = 'mentors'

    # Adding a constraint for the rating column
    __table_args__ = (CheckConstraint("rating <= 5 AND rating >= 1", name="check_ratings"),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    max_students = db.Column(db.Integer)
    current_students = db.Column(db.Integer) # API call / update query
    completed_students = db.Column(db.Integer) # API call / update query
    rating = db.Column(db.Integer) # Need to think about how we calculate this
    is_admin = db.Column(db.Boolean)

    # 1 to 1 relationship between users and mentors
    user = db.relationship('User', back_populates='mentors')

    # Many to 1 relationship between mentors and students 
    student = db.relationship('Student', back_populates='mentors', uselist=False)

    # 1 to Many relationship between mentors and support_logs
    support_logs = db.relationship('SupportLog', back_populates='mentors', uselist=False)

    @staticmethod
    def from_dict(dict):
        return Mentor(
            id = dict['id'],
            user_id = dict['user_id'],
            max_students = dict['max_students'],
            current_students = dict['current_students'],
            completed_students = dict['completed_students'],
            rating = dict['rating'],
            is_admin = dict['is_admin']
        )
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'max_students': self.max_students,
            'current_students': self.current_students,
            'completed_students': self.completed_students,
            'rating': self.rating,
            'is_admin': self.is_admin
        }
  

class Student(db.Model):

    """
    Data model for students
    """


    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id =  db.Column(db.Integer, db.ForeignKey(User.id))
    goals = db.Column(db.String(250))
    preferred_learning = db.Column(db.String(128))
    status = db.Column(db.String(128))
    start_date = db.Column(db.DateTime(timezone=True))
    end_date = db.Column(db.DateTime(timezone=True))
    mentor_id = db.Column(db.Integer, db.ForeignKey(Mentor.id))

    # 1 to 1 relationship between users and students
    user = db.relationship('User', back_populates='students')

    # Many to 1 relationship between students and mentors
    mentor = db.relationship('Mentor', back_populates='students')

    # 1 to Many relationship between students and support_logs
    support_logs = db.relationship('SupportLog', back_populates='students', uselist=False)

    @staticmethod
    def from_dict(dict):
        return Student(
            id = dict['id'],
            user_id = dict['user_id'],
            aims = dict['aims'],
            preferred_learning = dict['preferred_learning'],
            status = dict['status'],
            start_date = dict['start_date'],
            end_date = dict['end_date'],
            mentor_id = dict['mentor_id']
        )
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'aims': self.aims,
            'preferred_learning': self.preferred_learning,
            'status': self.status,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'mentor_id': self.mentor_id
        }
  
class Course(db.Model):

    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(128))
    is_active = db.Column(db.Boolean)


    @staticmethod
    def from_dict(dict):
        return Course(
            id = dict['id'],
            course_name = dict['course_name'],
            is_active = dict['is_active']
        )
    
    def to_dict(self):
        return {
            'id': self.id,
            'course_name': self.course_name,
            'is_active': self.is_active,
        }

class SupportLog(db.Model):

    __tablename__ = 'support_log'

    # Adding a constraint for the rating column
    __table_args__ = (CheckConstraint("mentor_assesment <= 5 AND mentor_assesment >= 1", name="check_mentor_assesment"),)

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    mentor_id = db.Column(db.Integer, db.ForeignKey(Mentor.id))
    student_id = db.Column(db.Integer, db.ForeignKey(Student.id))
    time_spent = db.Column(db.Integer)
    notes = db.Column(db.String(500))
    mentor_assesment = db.Column(db.Integer) # Struggle factor from 1-5. Can use this for 

    # Many to 1 relationship for support_logs and mentors
    mentor = db.relationship('Mentor', back_populates='support_log')

    # Many to 1 relationship for support_logs and students
    student = db.relationship('Student', back_populates='support_log')


    @staticmethod
    def from_dict(dict):
        return SupportLog(
            id = dict['id'],
            created_at = dict['created_at'],
            updated_at = dict['updated_at'],
            mentor_id = dict['mentor_id'],
            student_id = dict['student_id'],
            time_spent = dict['time_spent'],
            notes = dict['notes'],
            mentor_assesment = dict['mentor_assesment']
        )
    
    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'mentor_id': self.mentor_id,
            'student_id': self.student_id,
            'time_spent': self.time_spent,
            'notes': self.notes,
            'mentor_assesment': self.mentor_assesment
        }

class TimeZone(db.Model):

    __tablename__ = 'timezones'

    timezone = db.Column(db.String(128), primary_key=True)
    time_difference = db.Column(db.Integer)


# Association able betyween courses and users
user_courses = db.Table('user_courses',
                 db.Column('user_id', db.ForeignKey('users.id')),
                 db.Column('course_id', db.ForeignKey('courses.id'))
)
    