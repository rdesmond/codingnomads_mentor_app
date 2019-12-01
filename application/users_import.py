import requests
from models import User, Student, Mentor
from sqlalchemy import func
from . import db

# Getting the max created_at in the DB
# max_date = User.query(func.max(User.created_at)).scalar()


# Get all users created after max_date
# response = requests.get('URL')

# Inputting dummy data
users = {
    {
        'id':'1',
        'username': 'roger',
        'email': 'rogerpan95@gmail.com',
        'first_name': 'Roger',
        'last_name': 'Pan',
        'created_at': '2019-11-29 00:00:00',
        'telephone': '+447791109641',
        'learning_platform': 'roger',
        'forum': 'roger',
        'slack': 'roger',
        'timezone': 'UK/London',
        'bio': 'My name is Roger',
        'role': 'Student'
    }
}

# Creates a new user in the users table. Also creates a new row in the student or mentors table depending on their role. 
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
    
    


