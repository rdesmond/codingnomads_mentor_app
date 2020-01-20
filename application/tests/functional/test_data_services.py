from application.data_services import get_user, get_student_info
from application.models import User, Student, Mentor

def test_get_user(test_app, test_database, add_user):
    test_database.session.query(Student).delete()
    test_database.session.query(User).delete()

    user = add_user('testing_user')
    data = get_user(user.id)

    assert data is not None
    assert data.username == 'testing_user'
    assert data.id == 1


def test_get_student_info(test_app, test_database, add_user, add_student, add_mentor):
    test_database.session.query(Student).delete()
    test_database.session.query(User).delete()

    user1 = add_user('jonny', first_name="Jon", last_name='Doe')
    user2 = add_user('kristen', is_student=True)
    mentor = add_mentor(user1.id)
    student = add_student(user2.id)

    mentor.students.append(student)
    
    test_database.session.commit()

    data = get_student_info(student.id)


    assert data['username'] == 'kristen'
    assert data['mentor_name'] == 'Jon Doe'
    assert data['user_id'] == user2.id