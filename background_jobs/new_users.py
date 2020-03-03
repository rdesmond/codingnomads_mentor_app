import logging
from geoip import geolite2
import requests
from sqlalchemy import func
from application import db
from application.models import User, Student, Mentor, Course, UserCourse
from .config import MOODLE_API_URL


logging.basicConfig(filename='cron.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.DEBUG)

logging.info('1. Getting max created_at from the DB')
# Getting the max created_at in the DB
max_date = db.query(func.max(User.created_at)).scalar()
logging.info('1. Successfully extracted max created_at from the DB')

# Getting all users from Jon's endpoint which have been updated since the last user
users = requests.get(f'{MOODLE_API_URL}/api/users?updated={max_date}').json()

# Gets all user_ids from the D
current_users = db.query(User.id).all()

# Gets all courses in the DB
courses = db.query(Course.id).all()

# Inserts on confilct upserts a new user object for each user returned in the API
for id, data in users.items():
    # Creates a new user object
    new_user = User(
        id=data['id'],
        username=data['userName'],
        email=data['email'],
        first_name=data['firstName'],
        last_name=data['lastName'],
        first_access=data['firstAccess'],
        last_access=data['lastAccess'],
        last_login=data['lastLogin'],
        time_created=data['timeCreated'],
        time_modified=data['timeModified'],
        timezone=geolite2.lookup(data['lastIP']).timezone,
        is_student=data['student'],
        is_mentor=data['mentor'],
    )

    user_insert = db.session.add(new_user)

    user_update = user_insert.on_conflict_do_update(
        index_elements=['id'],
        set=dict(
            username=data['userName'],
            email=data['email'],
            first_name=data['firstName'],
            last_name=data['lastName'],
            first_access=data['firstAccess'],
            last_access=data['lastAccess'],
            last_login=data['lastLogin'],
            time_created=data['timeCreated'],
            time_modified=data['timeModified'],
            timezone=geolite2.lookup(data['lastIP']).timezone,
            is_student=data['student'],
            is_mentor=data['mentor'],
        )
    )


    # Creates a new student object if the user is a student
if data['student']:
    new_student = Student(user_id=data['id'])
    student_insert = db.session.add(new_student)
    student_update = student_insert.on_conflict_do_nothing(index_elements=['user_id'])


    # Creates a new mentor object if the user is a mentor
if data['mentor']:
    new_mentor = Mentor(user_id=data['id'], is_admin=False)  # Defaults to admin False
    mentor_insert = db.session.add(new_student)
    mentor_update = mentor_insert.on_conflict_do_nothing(index_elements=['user_id'])

    # Loops through all courses for the user
for course_id, course in data['courses'].items():

    # Checks whether it exists in courses and creates a new row if it doesn't
    if course_id not in courses:
        new_course = Course(id=course_id, course_name=course)
        db.session.add(new_course)

        # Creates a row for the association between users and courses
        user_course = UserCourse(user_id=id, course_id=course)
        user_course_insert = db.session.add(user_course)
        user_course_update = user_course_insert.on_conflict_do_nothing(index_elements=['user_id', 'course_id'])

# Commits all the changes
db.session.commit()
