from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta 
from sqlalchemy import Column, DateTime, event, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.ext.associationproxy import association_proxy
from geoip import geolite2
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

class User(db.Model, UserMixin):
    """
    Data model for users (students and mentors)
    """
    __tablename__ = 'users'

    # # Adding a constraint for the role column
    # __table_args__ = (CheckConstraint("role::text = ANY (ARRAY['student'::character varying, 'mentor'::character varying]::text[])", name="check_roles"),)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    first_access = db.Column(db.DateTime)
    last_access = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    time_created = db.Column(db.DateTime)
    time_modified = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    telephone = db.Column(db.String(128))
    learning_platform = db.Column(db.String(128))
    forum = db.Column(db.String(128))
    slack = db.Column(db.String(128))
    timezone = db.Column(db.String(128))
    bio = db.Column(db.String(500))
    is_student = db.Column(db.Boolean)
    is_mentor = db.Column(db.Boolean)

    # 1-1 relationship between users and mentors
    mentor = db.relationship('Mentor', backref=db.backref('user', uselist=False))

    # 1-1 relationship between users and students
    student = db.relationship('Student', backref=db.backref('user', uselist=False)) 

    # Many to many relationship between users and courses
    course = db.relationship('Course', secondary='user_courses', backref=db.backref('users', lazy='dynamic'))


    # user_courses = db.relationship('Course', secondary='user_courses', backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User {}>'.format(self.username)    
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def from_json(json):
        return User(
               id = json['id'], 
               username = json['userName'],
               email = json['email'],
               first_name = json['firstName'],
               last_name = json['lastName'],
               first_access = json['firstAccess'],
               last_access = json['lastAccess'],
               last_login = json['lastLogin'],
               time_created = json['timeCreated'],
               time_modified = json['timeModified'],
               timezone = geolite2.lookup(json['lastIP']).timezone,
               is_student = json['student'],
               is_mentor = json['mentor'],
        )
    
    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'first_access': self.first_access,
            'last_access': self.last_access,
            'last_login': self.last_login,
            'time_created': self.time_created,
            'time_modified':self.time_modified,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'telephone': self.telephone,
            'learning_platform': self.learning_platform,
            'forum': self.forum,
            'slack': self.slack,
            'timezone': self.timezone,
            'bio': self.bio,
            'role': self.role,
            'is_student': self.is_student,
            'is_mentor': self.is_mentor
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
    current_students = db.Column(db.Integer) 
    completed_students = db.Column(db.Integer) 
    rating = db.Column(db.Integer) # Need to think about how we calculate this
    is_admin = db.Column(db.Boolean)

    # 1-Many relationship between mentors and students
    students = db.relationship('Student', backref='mentor')

    def __repr__(self):
        return '<Mentor id: {}>'.format(self.id)    

    @staticmethod
    def from_dict(dict):
        return Mentor(
            user_id = dict['id'],
            max_students = dict['max_students'],
            current_students = dict['current_students'],
            completed_students = dict['completed_students'],
            rating = dict['rating'],
            is_admin = dict['is_admin'] # Need to modify criteria for this
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
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    mentor_id = db.Column(db.Integer, db.ForeignKey(Mentor.id))

    def __repr__(self):
        return '<Student id: {}>'.format(self.id)    

    @staticmethod
    def from_dict(dict):
        return Student(
            id = dict['id'],
            user_id = dict['user_id'],
            goals = dict['goals'],
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
            'goals': self.goals,
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
    end_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean)

    def __repr__(self):
        return '<Course id: {}>'.format(self.id)    


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
    support_type = db.Column(db.String(50), server_default='call')
    time_spent = db.Column(db.Integer)
    notes = db.Column(db.String(500))
    mentor_assesment = db.Column(db.Integer) # Struggle factor from 1-5. Can use this for 

    # Many to 1 relationship for support_logs and mentors
    mentor = db.relationship('Mentor', backref='support_log')

    # Many to 1 relationship for support_logs and students
    student = db.relationship('Student', backref='support_log')

    def __repr__(self):
        return '<SupportLog id: {}>'.format(self.id)    


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

# Association able betyween courses and users

class UserCourse(db.Model):

    __tablename__ = 'user_courses'

    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey(Course.id), primary_key=True)
    is_completed = db.Column(db.Boolean, server_default='False')

    user = db.relationship('User', backref=db.backref('user_courses', passive_deletes='all'))
    course = db.relationship('Course', backref=db.backref('user_courses', passive_deletes='all'))

