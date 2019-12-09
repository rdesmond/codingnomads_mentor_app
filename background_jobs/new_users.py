import requests
from application.models import User, Student, Mentor, Course, UserCourse
from sqlalchemy import func
from . import db
from geoip import geolite2

# Getting the max created_at in the DB
max_date = db.query(func.max(User.created_at)).scalar()

# Gets all courses in the DB
courses = db.query(Course)

# Get all users from Jon's endpoint and return as a json object
users = requests.get('base_url/api/users').json()

# # Dummy return from endpoint
# data = {
#     "23": {
#     "city": "Costa Mesa", 
#     "country": "US", 
#     "courses": {
#       "5": "Java Programming", 
#       "8": "Python Programming", 
#       "9": "Relearn to learn", 
#       "13": "Javascript Web Development", 
#       "14": "SQL & Databases", 
#       "20": "APIs and DBs With Python"
#     }, 
#     "currentLogin": 1568926111, 
#     "email": "cmullins510@gmail.com", 
#     "firstAccess": 1541695583, 
#     "firstName": "Cameron", 
#     "id": 23, 
#     "lastAccess": 1568926111, 
#     "lastIP": "173.25.136.166", 
#     "lastLogin": 1544066050, 
#     "lastName": "Mullins", 
#     "mentor": true, 
#     "roles": {
#       "3": "editingteacher", 
#       "5": "student"
#     }, 
#     "student": true, 
#     "timeCreated": 1541695476, 
#     "timeModified": 1544061334, 
#     "username": "cmullins"
# }


# Loop through the json object and check for timecreated after max_date
for id, data in users.items():
  # Creates a new user object
  if data['timeCreated'] > max_date:
    new_user = User(
               id = data['id'], 
               username = data['userName'],
               email = data['email'],
               first_name = data['firstName'],
               last_name = data['lastName'],
               first_access = data['firstAccess'],
               last_access = data['lastAccess'],
               last_login = data['lastLogin'],
               time_created = data['timeCreated'],
               time_modified = data['timeModified'],
               timezone = geolite2.lookup(data['lastIP']).timezone,
               is_student = True if data['student'] == 'true' else False,
               is_mentor = True if data['mentor'] == 'true' else False,
        )
    db.session.add(new_user)
  
  # Creates a new student object if the user is a student
  if data['student'] == 'true':
    new_student = Student(user_id=data['id']) # Need to also add the mentor_id of the student if already assignef
    db.session.add(new_student)

  # Creates a new mentor object if the user is a mentor
  if data['mentor'] == 'true':
    admin = False

    # Checks whether the user is an admin
    if '3' in data['roles'].keys():
      admin=True
    new_mentor = Mentor(user_id=data['id'],is_admin=admin)
    db.session.add(new_student)

  # Loops through all courses for the user
  for course_id, course in data['courses'].items():

    # Checks whether it exists in courses and creates a new row if it doesn't
    if course_id not in courses:
      new_course = Course(id=course_id, course_name=course)
      db.session.add(new_course)

      # Creates a row for the association between users and courses
      user_course = UserCourse(user_id=id, course_id=course)
      db.session.add(user_course)

# Commits all the changes
db.session.commit()

    
    


