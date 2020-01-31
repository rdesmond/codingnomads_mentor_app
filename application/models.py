from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import CheckConstraint
from geoip import geolite2
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """Data model for users (students and mentors)"""
    __tablename__ = 'users'

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
    is_student = db.Column(db.Boolean, nullable=False, default=False)
    is_mentor = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    preferences = db.relationship("UserPreferences", uselist=False, back_populates='user')

    # 1-1 relationship between users and mentors
    mentor = db.relationship('Mentor', uselist=False, back_populates='user')

    # 1-1 relationship between users and students
    student = db.relationship('Student', uselist=False, back_populates='user')

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
    def from_dict(dict):
        return User(
            id=dict['id'],
            username=dict['userName'],
            email=dict['email'],
            first_name=dict['firstName'],
            last_name=dict['lastName'],
            first_access=dict['firstAccess'],
            last_access=dict['lastAccess'],
            last_login=dict['lastLogin'],
            time_created=dict['timeCreated'],
            time_modified=dict['timeModified'],
            created_at=dict['created_at'],
            updated_at=dict['updated_at'],
            telephone=dict['telephone'],
            learning_platform=dict['learning_platform'],
            forum=dict['forum'],
            slack=dict['slack'],
            timezone=geolite2.lookup(dict['lastIP']).timezone,
            bio=dict['bio'],
            is_student=dict['is_student'],
            is_mentor=dict['is_mentor'],
            mentor=dict['mentor'],
            student=dict['student'],
            course=dict['course']
        )

    def to_dict(self):
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
            'time_modified': self.time_modified,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'telephone': self.telephone,
            'learning_platform': self.learning_platform,
            'forum': self.forum,
            'slack': self.slack,
            'timezone': self.timezone,
            'bio': self.bio,
            'is_student': self.is_student,
            'is_mentor': self.is_mentor,
            'is_admin': self.is_admin,
        }


class Mentor(db.Model):
    """Data model for mentors"""
    __tablename__ = 'mentors'

    # Adding a constraint for the rating column
    __table_args__ = (CheckConstraint("rating <= 5 AND rating >= 1", name="check_ratings"),)

    id = db.Column(db.Integer, primary_key=True)
    max_students = db.Column(db.Integer)
    current_students = db.Column(db.Integer)
    completed_students = db.Column(db.Integer)
    rating = db.Column(db.Integer)  # Need to think about how we calculate this

    # 1-Many relationship between mentors and students
    students = db.relationship('Student', back_populates='mentor')

    # support logs
    support_logs = db.relationship('SupportLog', back_populates='mentor')

    # user mentor relationship
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship('User', back_populates='mentor')

    def __repr__(self):
        return '<Mentor id: {}>'.format(self.id)

    @staticmethod
    def from_dict(dict):
        return Mentor(
            user_id=dict['id'],
            max_students=dict['max_students'],
            current_students=dict['current_students'],
            completed_students=dict['completed_students'],
            rating=dict['rating'],
        )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'max_students': self.max_students,
            'current_students': self.current_students,
            'completed_students': self.completed_students,
            'rating': self.rating,
        }


class Student(db.Model):
    """Data model for students."""
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    goals = db.Column(db.String(250))
    preferred_learning = db.Column(db.String(128))
    status = db.Column(db.String(128))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    # mentor relationship
    mentor_id = db.Column(db.Integer, db.ForeignKey(Mentor.id))
    mentor = db.relationship('Mentor', back_populates='students')

    # user student relationship
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship("User", back_populates='student')

    # student support logs
    support_logs = db.relationship("SupportLog", back_populates='student')

    def __repr__(self):
        return '<Student id: {}>'.format(self.id)

    @staticmethod
    def from_dict(dict):
        return Student(
            id=dict['id'],
            user_id=dict['user_id'],
            goals=dict['goals'],
            preferred_learning=dict['preferred_learning'],
            status=dict['status'],
            start_date=dict['start_date'],
            end_date=dict['end_date'],
            mentor_id=dict['mentor_id']
        )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'aims': self.goals,
            'preferred_learning': self.preferred_learning,
            'status': self.status,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'mentor_id': self.mentor_id
        }


class Course(db.Model):
    """Data model for courses."""
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(128))
    end_date = db.Column(db.DateTime)  # Maybe take out
    is_active = db.Column(db.Boolean)

    def __repr__(self):
        return '<Course id: {}>'.format(self.id)

    @staticmethod
    def from_dict(dict):
        return Course(
            id=dict['id'],
            course_name=dict['course_name'],
            is_active=dict['is_active']
        )

    def to_dict(self):
        return {
            'id': self.id,
            'course_name': self.course_name,
            'is_active': self.is_active,
        }


class SupportLog(db.Model):
    """A support log to keep track of mentor support given to a student."""
    __tablename__ = 'support_log'
    # Adding a constraint for the rating column
    __table_args__ = (CheckConstraint("comprehension <= 5 AND comprehension >= 1", name="check_comprehension"),)

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    support_type = db.Column(db.String(50), server_default='call')
    time_spent = db.Column(db.Integer)
    notes = db.Column(db.String(500))
    comprehension = db.Column(db.Integer)  # Struggle factor from 1-5


    # Many to 1 relationship for support_logs and mentors
    mentor_id = db.Column(db.Integer, db.ForeignKey(Mentor.id))
    mentor = db.relationship('Mentor', back_populates='support_logs')


    # Many to 1 relationship for support_logs and students
    student_id = db.Column(db.Integer, db.ForeignKey(Student.id))
    student = db.relationship('Student', back_populates='support_logs')


    def __repr__(self):
        return '<SupportLog id: {}>'.format(self.id)

    @staticmethod
    def from_dict(dict):
        return SupportLog(
            mentor_id=dict['mentor_id'],
            student_id=dict['student_id'],
            time_spent=dict['time_spent'],
            support_type=dict['support_type'],
            notes=dict['notes'],
            comprehension=dict['comprehension']
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
            'comprehension': self.comprehension,
            'support_type': self.support_type
        }


class UserCourse(db.Model):
    """Association table between courses and users."""
    __tablename__ = 'user_courses'

    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey(Course.id), primary_key=True)
    is_completed = db.Column(db.Boolean, server_default='False')

    user = db.relationship('User', backref=db.backref('user_courses', passive_deletes='all'))
    course = db.relationship('Course', backref=db.backref('user_courses', passive_deletes='all'))


class UserPreferences(db.Model):

    """User avaialability preferences"""
    __tablename__ = 'user_preferences'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey(User.id), unique=True)
    user = db.relationship('User', back_populates='preferences')

    monday = db.Column(db.Boolean, default=False)
    tuesday = db.Column(db.Boolean, default=False)
    wednesday = db.Column(db.Boolean, default=False)
    thursday = db.Column(db.Boolean, default=False)
    friday = db.Column(db.Boolean, default=False)
    saturday = db.Column(db.Boolean, default=False)
    sunday = db.Column(db.Boolean, default=False)
    start_hour = db.Column(db.Integer)
    end_hour = db.Column(db.Integer)

    def to_dict(self):
        return {
            'monday': self.monday,
            'tuesday': self.tuesday,
            'wednesday': self.wednesday,
            'thursday': self.thursday,
            'friday': self.friday,
            'saturday': self.saturday,
            'sunday': self.sunday,
            'start_hour': self.start_hour,
            'end_hour': self.end_hour,
        }


class StudentNote(db.Model):
    """model for mentors notes on students"""
    __tablename__ = 'student_notes'

    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey(User.id))
    student_id = db.Column(db.Integer, db.ForeignKey(User.id))
    note = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    @staticmethod
    def from_dict(dict):
        return StudentNote(
            mentor_id=dict['mentor_id'],
            student_id=dict['student_id'],
            note=dict['note'],
        )

    
    def to_dict(self):
        return {
            'id': self.id,
            'mentor_id': self.mentor_id,
            'student_id': self.student_id,
            'note': self.note,
            'created_at': self.created_at
        }