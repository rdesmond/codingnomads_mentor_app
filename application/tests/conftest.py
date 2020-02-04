import pytest
from datetime import datetime

from application import create_app, db
from application.models import User, Student, Mentor, SupportLog, UserPreferences


@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.config.from_object('application.config.TestingConfig')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all


@pytest.fixture(scope='function')
def test_database():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()





@pytest.fixture(scope='function')
def add_user():
    def _add_user(username, email="No email provided", password_hash=None, first_name=None, last_name=None,
                    first_access=None, last_access=None, time_created=None, time_modified=None,
                    created_at=None, updated_at=None, telephone=None, learning_platform=None,
                    forum=None, slack=None, timezone=None, bio=None, is_student=False, is_mentor=False,
                    is_admin=False):
        user = User(
            username = username,
            email = email,
            password_hash = password_hash,
            first_name = first_name,
            last_name = last_name,
            first_access = first_access,
            last_access = last_access,
            time_created = time_created,
            time_modified = time_modified,
            created_at = created_at,
            updated_at = updated_at,
            telephone = telephone,
            learning_platform = learning_platform,
            forum = forum,
            slack = slack,
            timezone = timezone,
            bio = bio,
            is_student = is_student,
            is_mentor = is_mentor,
            is_admin = is_admin,
        )
        db.session.add(user)
        db.session.commit()
        
        return user
    return _add_user


@pytest.fixture(scope='function')
def add_student():
    def _add_student(username, email='No email provided'):

        user = User(
            username=username,
            email=email,
            is_student=True

        )

        db.session.add(user)
        db.session.commit()

        db.session.add(UserPreferences(user_id=user.id))
        db.session.commit()
    
        student = Student(
            user_id = user.id,
        )

        db.session.add(student)
        db.session.commit()
        return user
    return _add_student


@pytest.fixture(scope='function')
def add_mentor():
    def _add_mentor(username, email='no email provided'):

        user = User(
            username=username,
            email=email,
            is_mentor=True
        )
        db.session.add(user)
        db.session.commit()

        db.session.add(UserPreferences(user_id=user.id))
        db.session.commit()
        
        mentor = Mentor(
            user_id = user.id
        )
        db.session.add(mentor)
        db.session.commit()

        return user
    return _add_mentor


@pytest.fixture(scope='function')
def add_support_log():
    def _add_support_log(mentor_id, student_id, support_type='call',
                        time_spent=0, notes=None, comprehension=1):
        support_log = SupportLog(
            mentor_id = mentor_id,
            student_id = student_id,
            support_type = support_type,
            time_spent = time_spent,
            notes = notes,
            comprehension = comprehension
        )
        
        db.session.add(support_log)
        db.session.commit()

        return support_log
    return _add_support_log



@pytest.fixture(scope='function')
def login():
    def _login(client, username, password):
        print(username, password)
        return client.post('/login', data=dict(
            username=username,
            password=password,
        ), follow_redirects=True)
    return _login


@pytest.fixture(scope='function')
def logout():
    def _logout(client):
        return client.get('/logout', follow_redirects=True)
    return _logout
