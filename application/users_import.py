import requests
from models import User, Student, Mentor
from sqlalchemy import func
from . import db

# Getting the max created_at in the DB
# max_date = User.query(func.max(User.created_at)).scalar()


# Get all users created after max_date
# response = requests.get('URL')

# Dummy data
data = '
    "4": {
    "currentlogin": 1568128077,
    "email": "cadenmackenzie@gmail.com",
    "firstaccess": 1538401309,
    "firstname": "Caden",
    "id": 4,
    "lastaccess": 1568128139,
    "lastlogin": 1566185569,
    "lastname": "Mackenzie",
    "mentor": true,
    "roles": [
        "student",
        "manager",
        "editingteacher",
        "coursecreator"
    ],
    "student": true,
    "username": "caden"
},'

# IF existis update / insert. Creates a new user in the users table. Also creates a new row in the student or mentors table depending on their role. 
for row in users:
    user = User.from_dict(user)
    db.session.add(user)
    if user.role == 'Student':
        student = Student(user_id=user.id)
        db.session.add(student)
        db.session.commit()
    elif user.role == 'Mentor':
        mentor = Mentor(user_id=user.id)
        db.session.add(mentor)
        db.session.commit()
    
    


