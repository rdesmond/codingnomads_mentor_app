import pytest
from datetime import datetime

from application import create_app, db
from application.models import User


@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.config.from_object('application.config.TestingConfig')
    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def test_database():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='function')
def add_user():
    def _add_user(firstname, is_student, is_mentor):
        user = User(
            username = f'{firstname}-username',
            email = f'{firstname}@mentorportal.com',
            password_hash = f'{firstname}-password',
            first_name = f'{firstname}',
            last_name = 'smith',
            first_access = datetime.utcnow(),
            last_access = datetime.utcnow(),
            time_created = datetime.utcnow(),
            time_modified = datetime.utcnow(),
            created_at = datetime.utcnow(),
            updated_at = datetime.utcnow(),
            telephone = '800-555-5555',
            learning_platform = 'Python',
            forum = f'{firstname}-forum',
            slack = f'{firstname}-slack',
            timezone = 'EST',
            bio = f'{firstname}-bio',
            is_student = is_student,
            is_mentor = is_mentor

        )
        db.session.add(user)
        db.session.commit()
        return user
    return _add_user