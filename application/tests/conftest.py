import pytest
from datetime import datetime

from application import create_app, db
from application.models import User, Student, Mentor


@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.config.from_object('application.config.TestingConfig')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all


@pytest.fixture(scope='module')
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
    def _add_student(user_id, goals=None, preferred_learning=None, status=None,
                    start_date=None, end_date=None, mentor_id=None):
    
        student = Student(
            user_id = user_id,
            goals = goals,
            preferred_learning = preferred_learning,
            status = status,
            start_date = start_date,
            end_date = end_date,
            mentor_id = mentor_id,
        )

        db.session.add(student)
        db.session.commit()
        return student
    return _add_student


@pytest.fixture(scope='function')
def add_mentor():
    def _add_mentor(user_id, max_students=None, current_students=None,
                    completed_students=None, rating=None):
        
        mentor = Mentor(
            user_id = user_id,
            max_students = max_students,
            current_students = current_students,
            completed_students = completed_students,
            rating = rating
        )
        db.session.add(mentor)
        db.session.commit()

        return mentor
    return _add_mentor