from . import db
from sqlalchemy import text
from .models import User, Student, Course, SupportLog, Mentor, UserPreferences, StudentNote



def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


def get_student_info(user_id):
    """Fetches info about a student, given their ID."""

    data = {}

    user = User.query.filter_by(id=user_id).first()
    if not user or user.is_student == False:
        return None

    preferences = UserPreferences.query.filter_by(user_id=user.id).first()
    mentor = Mentor.query.filter_by(id=user.student.mentor_id).first()

    data = {
        "aims": user.student.goals,
        "id": user.id,
        "mentor_id": user.student.mentor_id,
        "mentor_name": f'{mentor.user.first_name} {mentor.user.last_name}' if mentor else None,
        "preferred_learning": user.student.preferred_learning,
        "start_date": user.student.start_date,
        "status": user.student.status,
        "student_id": user.student.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "learning_platform": user.learning_platform,
        "forum": user.forum,
        "slack": user.slack,
        "time_zone": user.timezone,
        "courses": [course.to_dict() for course in user.user_courses],
        "preferred_days": {
                "Mon": preferences.monday if preferences else None, 
                "Tue": preferences.tuesday if preferences else None, 
                "Wed": preferences.wednesday if preferences else None,
                "Thu": preferences.thursday if preferences else None,
                "Fri": preferences.friday if preferences else None,
                "Sat": preferences.saturday if preferences else None,
                "Sun": preferences.sunday if preferences else None,
            },
        "preferred_start_time": preferences.start_hour if preferences else None,
        "preferred_end_time": preferences.end_hour if preferences else None,
    }
    
    return data



def get_mentor_info(user_id):
    """Fetches info about a mentor, given their ID."""

    user = User.query.filter_by(id=user_id).first()
    
    if not user or user.is_mentor == False:
        return None

    preferences = UserPreferences.query.filter_by(user_id=user.id).first()


    data = {
            "completed_students": user.mentor.completed_students,
            "current_students": user.mentor.current_students,
            "id": user.id,
            "is_admin": user.is_admin,
            "max_students": user.mentor.max_students,
            "rating": user.mentor.rating,
            "mentor_id": user.mentor.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "learning_platform": user.learning_platform,
            "forum": user.forum,
            "slack": user.slack,
            "time_zone": user.timezone,
            "preferred_days": {
                "Mon": preferences.monday if preferences else None, 
                "Tue": preferences.tuesday if preferences else None, 
                "Wed": preferences.wednesday if preferences else None,
                "Thu": preferences.thursday if preferences else None,
                "Fri": preferences.friday if preferences else None,
                "Sat": preferences.saturday if preferences else None,
                "Sun": preferences.sunday if preferences else None,
            },
            "preferred_start_time": preferences.start_hour if preferences else None,
            "preferred_end_time": preferences.end_hour if preferences else None,
        }


    return data



def get_mentor_info_with_students(user_id):

    user = User.query.filter_by(id=user_id).first()

    if not user or user.is_mentor == False:
        return None

    student_ids = [student.user.id for student in user.mentor.students]

    data = {
        'mentor': get_mentor_info(user_id),
        'students': [get_student_info(id) for id in student_ids],
    }

    return data



def log_student_support(log: dict) -> str:
    """Create a support log for a student.
    """
    support_log = SupportLog.from_dict(log)

    db.session.add(support_log)
    db.session.commit()
    return 'Support log successfully added'


def get_student_support_logs(user_id):
    """Get all support logs for a given student."""
    data = None
    user = User.query.filter_by(id=user_id).first()
    logs = user.student.support_logs
    if logs:
        data = [log.to_dict() for log in logs]
    return data


def get_all_students():
    """Fetch all students from the database."""
    data = []
    students = Student.query.all()
    for student in students:
        data.append(student.to_dict())
    return data


def assign_students_to_mentor(student_id, mentor_id):
    """Assigns a student to a mentor by adding the mentor_id for a given student to their DB entry."""
    student = Student.query.filter_by(id=student_id).first()
    student.mentor_id = mentor_id
    db.session.commit()
    return f'student id:{student.id} successfully assigned to mentor id:{student.mentor_id}'


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


