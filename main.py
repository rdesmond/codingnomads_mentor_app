from application import create_app, db
from application.models import User, Student, Mentor, UserPreferences, SupportLog, Course
from flask.cli import FlaskGroup

app = create_app()

cli = FlaskGroup(create_app=create_app)

@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command('seed_db')
def seed_db():
    user1 = User(username='jonny', email='jonny@test.com',first_name='Jonny', last_name='Doe', is_mentor=True)
    user2 = User(username='kristen', email='kristen@test.com',first_name='Kristen', last_name='Anderson', is_student=True)
    admin = User(username='admin', email='admin@test.com', is_admin=True)

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(admin)
    db.session.commit()

    user1.set_password('password')
    user2.set_password('password')
    admin.set_password('password')

    db.session.commit()

    preferences1 = UserPreferences(user_id=user1.id)
    preferences2 = UserPreferences(user_id=user2.id)
    preferences3 = UserPreferences(user_id=admin.id)

    db.session.add(preferences1)
    db.session.add(preferences2)
    db.session.add(preferences3)

    student = Student(user_id=user2.id)
    db.session.add(student)
    
    mentor = Mentor(user_id=user1.id)
    db.session.add(mentor)
    db.session.commit()

    user1.students.append(user2)
    db.session.commit()

    support_log = SupportLog(
        mentor_id = user1.id,
        student_id = user2.id,
        time_spent = 20,
        notes = 'This is a note',
        comprehension = 2
    )
    db.session.add(support_log)
    db.session.commit()

if __name__ == "__main__":
    cli()