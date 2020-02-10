from . import db
from sqlalchemy import text
from .models import User, Student, Course, SupportLog, Mentor, UserPreferences, StudentNote



def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


def get_all_students():
    """Fetch all students from the database."""

    data = []
    students = Student.query.all()
    for student in students:
        data.append(student.to_dict())
        
    return data


def build_mentor_object(user_object):
    return {
            "completed_students": user_object.mentor.completed_students,
            "current_students": user_object.mentor.current_students,
            "id": user_object.id,
            "is_admin": user_object.is_admin,
            "max_students": user_object.mentor.max_students,
            "rating": user_object.mentor.rating,
            "mentor_id": user_object.mentor.id,
            "username": user_object.username,
            "email": user_object.email,
            "first_name": user_object.first_name,
            "last_name": user_object.last_name,
            "learning_platform": user_object.learning_platform,
            "forum": user_object.forum,
            "slack": user_object.slack,
            "time_zone": user_object.timezone,
            "preferred_days": {
                "Mon": user_object.preferences.monday, 
                "Tue": user_object.preferences.tuesday, 
                "Wed": user_object.preferences.wednesday,
                "Thu": user_object.preferences.thursday,
                "Fri": user_object.preferences.friday,
                "Sat": user_object.preferences.saturday,
                "Sun": user_object.preferences.sunday,
            },
            "preferred_start_time": user_object.preferences.start_hour,
            "preferred_end_time": user_object.preferences.end_hour,
        }


def build_student_object(user_object, mentor_user_object):
    return {
        "aims": user_object.student.goals,
        "id": user_object.id,
        "mentor_id": mentor_user_object.id if mentor_user_object else None,
        "mentor_name": f'{mentor_user_object.first_name} {mentor_user_object.last_name}' if mentor_user_object else None,
        "preferred_learning": user_object.student.preferred_learning,
        "start_date": user_object.student.start_date,
        "status": user_object.student.status,
        "student_id": user_object.student.id,
        "username": user_object.username,
        "email": user_object.email,
        "first_name": user_object.first_name,
        "last_name": user_object.last_name,
        "learning_platform": user_object.learning_platform,
        "forum": user_object.forum,
        "slack": user_object.slack,
        "time_zone": user_object.timezone,
        "courses": [course.to_dict() for course in user_object.user_courses],
        "preferred_days": {
                "Mon": user_object.preferences.monday, 
                "Tue": user_object.preferences.tuesday, 
                "Wed": user_object.preferences.wednesday,
                "Thu": user_object.preferences.thursday,
                "Fri": user_object.preferences.friday,
                "Sat": user_object.preferences.saturday,
                "Sun": user_object.preferences.sunday,
            },
        "preferred_start_time": user_object.preferences.start_hour,
        "preferred_end_time": user_object.preferences.end_hour,
    }


def get_student_info(user_id):
    """Fetches info about a student, given their ID."""

    data = {}

    user = User.query.filter_by(id=user_id).first()
    if not user or user.is_student == False:
        return None

    mentor = User.query.filter_by(id=user.current_mentor).first()

    data = build_student_object(user, mentor)
    
    return data


def get_all_student_info():

    student_list = []

    students = User.query.filter_by(is_student=True).all()

    #TODO: query mentor for each student

    for user in students:
        student_list.append(build_student_object(user, mentor_user_object=None))

    return student_list


def get_mentor_info(user_id):
    """Fetches info about a mentor, given their ID."""

    user = User.query.filter_by(id=user_id).first()
    if not user or user.is_mentor == False:
        return None

    preferences = UserPreferences.query.filter_by(user_id=user.id).first()

    data = build_mentor_object(user)

    return data


def get_all_mentor_info():

    mentor_list = []

    mentors = User.query.filter_by(is_mentor=True).all()

    if mentors:
        for user in mentors:
            mentor_list.append(build_mentor_object(user))

    return mentor_list
    

def get_mentor_info_with_students(user_id):

    data = {}

    user = User.query.filter_by(id=user_id).first()
    if not user or user.is_mentor == False:
        return None

    data = build_mentor_object(user)

    student_ids = [student.id for student in user.students]
    students = User.query.filter(User.id.in_(student_ids)).all()
    data['students'] = [build_student_object(student, user) for student in students]

    return data






def get_student_support_logs(user_id):
    """Get all support logs for a given student."""

    data = None
    logs = SupportLog.query.filter_by(student_id=user_id).all()
    if logs:
        data = [log.to_dict() for log in logs]
    return data


def assign_students_to_mentor(mentor_user_id, student_user_id):
    """Assigns a student to a mentor by adding the mentor_id for a given student to their DB entry."""

    mentor = User.query.filter_by(id=mentor_user_id).first()
    student = User.query.filter_by(id=student_user_id).first()
    mentor.students.append(student)
    db.session.commit()

    return f'student id:{student.id} successfully assigned to mentor id:{mentor.id}'


def get_mentors_and_students():
    student_mentors_query = """
    SELECT
        s.user_id AS student_id,
        u.first_name||' '||u.last_name AS student_name,
        m.user_id AS mentor_id,
        um.first_name||' '||um.last_name AS mentor_name
    FROM
        students AS s
    LEFT JOIN 
        mentors AS m
    ON
        m.id = s.mentor_id
    LEFT JOIN
        users AS u
    ON
        u.id = s.user_id
    LEFT JOIN
        users AS um
    ON
        um.id = m.user_id;
    """
    student_mentors_proxy = db.engine.execute(text(student_mentors_query)).fetchall()
    data = [dict(row) for row in student_mentors_proxy]
    return data


def get_students_with_courses():
    students_query = """
    SELECT
        s.user_id,
        u.first_name||' '||u.last_name AS name,
        uc.course_id,
        c.course_name
    FROM
        students AS s
    INNER JOIN
        users AS u
    ON
        u.id = s.user_id
    LEFT JOIN
        user_courses AS uc
    ON
        uc.user_id = s.user_id
    LEFT JOIN
        courses AS c
    ON
        c.id = uc.course_id
    ORDER BY
        user_id ASC;
    """
    students_proxy = db.engine.execute(text(students_query)).fetchall()
    data = [dict(row) for row in students_proxy]
    return data


def get_mentors_with_courses():
    mentors_query = """
    SELECT
        m.user_id,
        u.first_name||' '||u.last_name AS name,
        uc.course_id,
        c.course_name
    FROM
        mentors AS m
    INNER JOIN
        users AS u
    ON
        u.id = m.user_id
    LEFT JOIN
        user_courses AS uc
    ON
        uc.user_id = m.user_id
    LEFT JOIN
        courses AS c
    ON
        c.id = uc.course_id
    ORDER BY
        user_id ASC;
    """
    mentors_proxy = db.engine.execute(text(mentors_query)).fetchall()
    data = [dict(row) for row in mentors_proxy]
    return data


def add_student_note(note: dict) -> str:

    note = StudentNote.from_dict(note)

    db.session.add(note)
    db.session.commit()

    return 'note successfully created'


def get_student_notes_by_mentor(user_id):
    
    data = []

    notes = StudentNote.query.filter_by(mentor_id=user_id).all()
    if notes:
        data = [note.to_dict() for note in notes]

    return data


def get_student_notes_by_student(user_id):

    data = []

    notes = StudentNote.query.filter_by(student_id=user_id).all()
    if notes:
        data = [note.to_dict() for note in notes]

    return data



def log_student_support(log: dict) -> str:
    """Create a support log for a student."""

    support_log = SupportLog.from_dict(log)
    db.session.add(support_log)
    db.session.commit()

    return 'Support log successfully added'


def get_support_logs_by_mentor(user_id):

    data = []

    logs = SupportLog.query.filter_by(mentor_id=user_id).all()
    if logs:
        data = [log.to_dict() for log in logs]

    return data