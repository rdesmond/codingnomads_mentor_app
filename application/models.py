from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """
    Data model for users (students and mentors)
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    # created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # updated_at = db.Column(db.DateTime(timezone=True),server_default=func.now(), onupdate=datetime.datetime.now)
    telephone = db.Column(db.String(128))
    learning_platform = db.Column(db.String(128))
    forum = db.Column(db.String(128))
    slack = db.Column(db.String(128))
    timezone = db.Column(db.String(128))
    bio = db.Column(db.String(500))
    role = db.Column(db.String(500))

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

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    max_students = db.Column(db.Integer)
    current_students = db.Column(db.Integer)
    completed_students = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    is_admin = db.Column(db.Boolean)

    # 1 to 1 relationship between users and mentors
    user = db.relationship('User', back_populates='mentors')

    # Many to 1 relationship between mentors and students 
    student = db.relationship('Student', back_populates='mentors', uselist=False)

    # 1 to Many relationship between mentors and support_logs
    support_logs = db.relationship('SupportLog', back_populates='mentors', uselist=False)
  

class Student(db.Model):

    """
    Data model for students
    """


    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id =  db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    aims = db.Column(db.String(128))
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
  


class Course(db.Model):

    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(128))
    is_active = db.Column(db.Boolean)

class SupportLog(db.Model):

    __tablename__ = 'support_log'

    id = db.Column(db.Integer, primary_key=True)
    # created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # updated_at = db.Column(db.DateTime(timezone=True),server_default=func.now(), onupdate=datetime.datetime.now)
    mentor_id = db.Column(db.Integer, db.ForeignKey(User.id))
    student_id = db.Column(db.Integer, db.ForeignKey(User.id))
    time_spent = db.Column(db.Integer)
    notes = db.Column(db.String(500))
    mentor_assesment = db.Column(db.String(500))

    # Many to 1 relationship for support_logs and mentors
    mentor = db.relationship('Mentor', back_populates='support_log')

    # Many to 1 relationship for support_logs and students
    student = db.relationship('Student', back_populates='support_log')

class TimeZone(db.Model):

    __tablename__ = 'timezones'

    timezone = db.Column(db.String(128), primary_key=True)
    time_difference = db.Column(db.Integer)


# Association able betyween courses and users
user_courses = db.Table('user_courses',
                 db.Column('user_id', db.ForeignKey('users.id')),
                 db.Column('course_id', db.ForeignKey('courses.id'))
)
    