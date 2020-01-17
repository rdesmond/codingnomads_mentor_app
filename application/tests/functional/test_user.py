from application.models import User
import json


def test_add_single_user(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    user = add_user(firstname = 'jonny', is_student=False, is_mentor=False)
    data = User.query.filter_by(id=user.id).first()
    assert data.username == 'jonny-username'
    assert data.email == 'jonny@mentorportal.com'
    assert data.is_mentor == False
    assert data.is_student == False


def test_add_muliple_users(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    user1 = add_user(firstname='jonny', is_student=False, is_mentor=False)
    user2 = add_user(firstname='kristen', is_student=True, is_mentor=False)
    data = User.query.all()
    assert data[0].username == 'jonny-username'
    assert data[0].email == 'jonny@mentorportal.com'
    assert data[0].is_student == False
    assert data[0].is_mentor == False
    assert data[1].username == 'kristen-username'
    assert data[1].email == 'kristen@mentorportal.com'
    assert data[1].is_student == True
    assert data[1].is_mentor == False