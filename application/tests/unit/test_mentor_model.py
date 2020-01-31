from application.models import User, Mentor, Student


def test_add_mentor(test_app, test_database, add_user):
    test_database.session.query(Mentor).delete()
    test_database.session.query(User).delete()

    user = add_user(username='jonny', is_mentor=True)

    mentor = Mentor(
        user_id = user.id,
        max_students = 5,
        current_students = 1,
        completed_students = 0,
        rating = 2,
    )

    test_database.session.add(mentor)
    test_database.session.commit()

    mentor = Mentor.query.filter_by(user_id=user.id).first()

    assert mentor.user_id == user.id
    assert mentor.rating == 2
    assert mentor.user.username == 'jonny'


def test_add_multiple_mentors(test_app, test_database, add_user):
    test_database.session.query(Mentor).delete()
    test_database.session.query(User).delete()

    user1 = add_user(username='jonny', is_mentor=True)
    user2 = add_user(username='kristen', is_mentor=True)

    mentor1 = Mentor(
        user_id = user1.id,
        max_students = 5,
        current_students = 1,
        completed_students = 0,
        rating = 2,
    )

    mentor2 = Mentor(
        user_id = user2.id,
        max_students = 1,
        current_students = 1,
        completed_students = 0,
        rating = 2,
    )

    test_database.session.add(mentor1)
    test_database.session.add(mentor2)
    test_database.session.commit()
    
    mentor1 = Mentor.query.filter_by(user_id=user1.id).first()
    mentor2 = Mentor.query.filter_by(user_id=user2.id).first()
    all_mentors = Mentor.query.all()

    assert mentor1.user.username == 'jonny'
    assert mentor1.user.id == user1.id
    assert mentor2.user.username == 'kristen'
    assert mentor2.user.id == user2.id
    assert len(all_mentors) == 2


def test_add_student_to_mentor(test_app, test_database, add_user, add_student, add_mentor):
    test_database.session.query(Student).delete()
    test_database.session.query(Mentor).delete()
    test_database.session.query(User).delete()
    
    mentor = add_mentor('jonny')
    student = add_student('kristen')

    mentor.students.append(student)

    students = mentor.students.all()



    assert mentor.username == 'jonny'
    assert student.username == 'kristen'
    assert len(students) == 1
    assert students[0].username == 'kristen'
