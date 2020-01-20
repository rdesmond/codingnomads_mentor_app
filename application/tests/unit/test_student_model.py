from application.models import User, Student



def test_add_student(test_app, test_database, add_user):
    test_database.session.query(Student).delete()
    test_database.session.query(User).delete()
    user = add_user(username='jonny', is_student=True)

    student = Student(
            user_id = user.id,
            goals = 'get job',
            preferred_learning = 'one on one',
            status = 'active',
            start_date = None,
            end_date = None,
            mentor_id = None
        )

    test_database.session.add(student)
    test_database.session.commit()

    student = Student.query.filter_by(user_id=user.id).first()



    assert student.user_id == user.id
    assert student.user.username == 'jonny'



def test_add_multiple_students(test_app, test_database, add_user):
    test_database.session.query(Student).delete()
    test_database.session.query(User).delete()
    user1 = add_user(username='jonny', is_student=True)
    user2 = add_user(username='kristen', is_student=True)
    
    student1 = Student(
            user_id = user1.id,
            goals = 'get job',
            preferred_learning = 'one on one',
            status = 'active',
            start_date = None,
            end_date = None,
            mentor_id = None
        )

    test_database.session.add(student1)
    test_database.session.commit()

    student2 = Student(
            user_id = user2.id,
            goals = 'get job',
            preferred_learning = 'one on one',
            status = 'active',
            start_date = None,
            end_date = None,
            mentor_id = None
        )

    test_database.session.add(student2)
    test_database.session.commit()

    students = Student.query.all()


    assert students[0].user_id == user1.id
    assert students[0].user.username == 'jonny'
    assert students[1].user_id == user2.id
    assert students[1].user.username == 'kristen'
    assert len(students) == 2


def test_user_student_relationship(test_app, test_database, add_user, add_student):
    test_database.session.query(Student).delete()
    test_database.session.query(User).delete()
    user = add_user(username='jonny', is_student=True)
    student = add_student(user.id)

    assert user.id == user.student.user_id
    assert student.user.username == 'jonny'
    