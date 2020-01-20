from application.models import User, Student
import json


def test_add_single_user(test_app, test_database):
    test_database.session.query(Student).delete()
    test_database.session.query(User).delete()

    firstname = 'jonny'

    user = User(
            username = 'jonny',
            email = 'jonny@mentorportal.com',
            password_hash = 'password',
            first_name = 'jonny',
            last_name = 'smith',
            first_access = None,
            last_access = None,
            time_created = None,
            time_modified = None,
            created_at = None,
            updated_at = None,
            telephone = '800-555-5555',
            learning_platform = 'Python',
            forum = None,
            slack = None,
            timezone = 'EST',
            bio = None,
            is_student = False,
            is_mentor = False,
            is_admin = False
        )
    test_database.session.add(user)
    test_database.session.commit()

    data = User.query.filter_by(id=user.id).first()
    assert data.username == 'jonny'
    assert data.email == 'jonny@mentorportal.com'
    assert data.is_mentor == False
    assert data.is_student == False


def test_add_muliple_users(test_app, test_database):
    test_database.session.query(Student).delete()
    test_database.session.query(User).delete()

    user1 = User(
            username = 'jonny',
            email = 'jonny@mentorportal.com',
            password_hash = 'password',
            first_name = 'jonny',
            last_name = 'smith',
            first_access = None,
            last_access = None,
            time_created = None,
            time_modified = None,
            created_at = None,
            updated_at = None,
            telephone = '800-555-5555',
            learning_platform = 'Python',
            forum = None,
            slack = None,
            timezone = 'EST',
            bio = None,
            is_student = False,
            is_mentor = False,
            is_admin = False
        )
    test_database.session.add(user1)
    test_database.session.commit()

    user2 = User(
            username = 'kristen',
            email = 'kristen@mentorportal.com',
            password_hash = 'password',
            first_name = 'kristen',
            last_name = 'smith',
            first_access = None,
            last_access = None,
            time_created = None,
            time_modified = None,
            created_at = None,
            updated_at = None,
            telephone = '800-555-5555',
            learning_platform = 'Python',
            forum = None,
            slack = None,
            timezone = 'EST',
            bio = None,
            is_student = True,
            is_mentor = False,
            is_admin = False
        )
    test_database.session.add(user2)
    test_database.session.commit()


    data = User.query.all()
    assert data[0].username == 'jonny'
    assert data[0].email == 'jonny@mentorportal.com'
    assert data[0].is_student == False
    assert data[0].is_mentor == False
    assert data[1].username == 'kristen'
    assert data[1].email == 'kristen@mentorportal.com'
    assert data[1].is_student == True
    assert data[1].is_mentor == False
