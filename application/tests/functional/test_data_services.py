from application.data_services import *
from application.models import User, Student, Mentor, UserPreferences, StudentNote, mentor_student_assignments, StudentNote



def test_get_user(test_app, test_database, add_user):


    user = add_user('testing_user')
    data = get_user(user.id)

    assert data is not None
    assert data.username == 'testing_user'
    assert data.id == 1


def test_get_student_info(test_app, test_database, add_user, add_student):


    student = add_student('kristen')

    data = get_student_info(student.id)


    assert data['username'] == 'kristen'
    assert data['id'] == student.id
    assert len(data['courses']) == 0
    assert data['preferred_days']['Mon'] == False


def test_get_student_support_logs(test_app, test_database, add_user, add_student, add_mentor, add_support_log):



    mentor = add_mentor('jonny')
    student = add_student('kristen')

    add_support_log(mentor.id, student.id)

    data = get_student_support_logs(student.id)

    assert len(data) == 1
    assert data[0]['mentor_id'] == mentor.id
    assert data[0]['student_id'] == student.id
    assert data[0]['support_type'] == 'call'


def test_get_mentor_info(test_app, test_database, add_user, add_mentor):

    mentor = add_mentor('jonny')

    data = get_mentor_info(mentor.id)


    assert data is not None
    assert data['username'] == 'jonny'


def test_log_student_support(test_app, test_database, add_user, add_mentor, add_student):

   
    student = add_student('kristen')
    mentor = add_mentor('jonny')

    log = {
        'mentor_id': mentor.id,
        'student_id': student.id,
        'time_spent': 20,
        'support_type': 'chat',
        'notes': 'This is a note',
        'comprehension': 2
    }

    log_student_support(log)

    support_log = SupportLog.query.filter_by(mentor_id=mentor.id).first()

    assert support_log.student_id == student.id
    assert support_log.support_type == 'chat'


def test_get_student_support_logs(test_app, test_database, add_student, add_mentor, add_support_log):


    mentor = add_mentor('jonny')
    student = add_student('kristen')

    support_log_1 = add_support_log(mentor.id, student.id)
    support_log_2 = add_support_log(mentor.id, student.id)

    logs = get_student_support_logs(student.id)

    assert logs
    assert len(logs) == 2
    assert logs[0]['student_id'] == student.id


def test_get_all_students(test_app, test_database, add_student):


    add_student('jonny')
    add_student('kristen')

    data = get_all_students()

    assert len(data) == 2


def test_assign_students_to_mentor(test_app, test_database, add_student, add_mentor):


    mentor = add_mentor('jonny')
    student = add_student('kristen')

    result = assign_students_to_mentor(mentor.id, student.id)

    assert result == f'student id:{student.id} successfully assigned to mentor id:{mentor.id}'
    assert mentor.students[0].id == student.id
    assert mentor.students[0].username == 'kristen'


def test_get_mentor_info_with_students(test_app, test_database, add_student, add_mentor):

    mentor = add_mentor('jonny')
    student1 = add_student('kristen')
    student2 = add_student('billy')

    mentor.students.append(student1)
    mentor.students.append(student2)


    data = get_mentor_info_with_students(mentor.id)

    assert data
    assert len(data['students']) == 2
    assert student1 in mentor.students


def test_add_note(test_app, test_database, add_mentor, add_student):

  
    mentor = add_mentor('jonny')
    student = add_student('kristen')

    note = {
        'mentor_id': mentor.id,
        'student_id': student.id,
        'note': 'this is a test note'
    }

    result = add_student_note(note)

    data = (StudentNote.query.filter_by(mentor_id = mentor.id).first()).to_dict()
    
    assert result == 'note successfully created'
    assert data['mentor_id'] == mentor.id
    assert data['student_id'] == student.id
    assert data['note'] == "this is a test note"

def test_get_student_notes_by_mentor(test_app, test_database, add_mentor, add_student):
    
    mentor = add_mentor('jonny')
    student = add_student('kristen')

    note1 = StudentNote.from_dict({
        'mentor_id': mentor.id,
        'student_id': student.id,
        'note': 'this is a test note'
    })

    note2 = StudentNote.from_dict({
        'mentor_id': mentor.id,
        'student_id': student.id,
        'note': 'this is a test note #2'
    })

    test_database.session.add(note1)
    test_database.session.add(note2)
    test_database.session.commit()

    data = get_student_notes_by_mentor(mentor.id)

    assert len(data) == 2
    assert data[0]['note'] == 'this is a test note'
    assert data[0]['mentor_id'] == 1


def test_get_all_student_info(test_app, test_database, add_student):

    student1 = add_student('jonny')
    student2 = add_student('kristen')

    data = get_all_student_info()

    assert len(data) == 2
    assert data[0]['username'] == 'jonny'


def test_get_all_mentor_info(test_app, test_database, add_mentor):

    mentor1 = add_mentor('jonny')
    mentor2 = add_mentor('kristen')

    data = get_all_mentor_info()

    assert len(data) == 2
    assert data[0]['username'] == 'jonny'


def test_get_support_logs_by_mentor(test_app, test_database, add_mentor, add_student, add_support_log):

    mentor = add_mentor('jonny')
    student = add_student('kristen')
    
    add_support_log(mentor.id, student.id)
    add_support_log(mentor.id, student.id)

    data = get_support_logs_by_mentor(mentor.id)

    assert len(data) == 2
    assert data[0]['student_id'] == student.id