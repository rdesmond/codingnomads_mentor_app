from . import db
from sqlalchemy import text
from .models import User, Student, Course, SupportLog, Mentor


def get_student_info(student_id):
    """Fetches info about a student, given their ID."""
    # TODO: build out DB calls so it has all the necessary info (as described in the specs)
    data = None
    student = Student.query.filter(Student.id == student_id).first()
    if student:
        data = student.to_dict()
    return data


def get_mentor_info(mentor_id):
    """Fetches info about a mentor, given their ID."""
    # TODO: build out DB calls so it has all the necessary info (as described in the specs)
    data = None
    mentor = Mentor.query.filter(Mentor.id == mentor_id).first()
    if mentor:
        data = mentor.to_dict()
    return data


def log_student_support(mentor_id, student_id, support_type, time_spent, notes, comprehension):
    """Create a support log for a student."""
    support_log = SupportLog(
        mentor_id=mentor_id,
        student_id=student_id,
        support_type=support_type,
        time_spent=time_spent,
        notes=notes,
        comprehension=comprehension
    )
    db.session.add(support_log)
    db.session.commit()
    return 'Support log successfully added'


def get_student_support_logs(student_id):
    """Get all support logs for a given student."""
    data = None
    #logs = SupportLog.query.filter(SupportLog.mentor_id == mentor_id).filter(SupportLog.student_id == student_id).all()
    # Note: IMO it's important to see all support logs for a student, even if done by a different mentor
    logs = SupportLog.query.filter(SupportLog.student_id == student_id).all()
    if logs:
        data = [log.to_dict() for log in logs]
    return data


def get_student_overview(id):
    # TODO: what was this call about? seems to get info about the student (+some), maybe should be related to mentor?
    data = None
    query = """
    SELECT
        s.user_id,
        uc.course_id,
        c.course_name
    FROM
        students AS s
    LEFT JOIN
        user_courses AS uc
    ON
        uc.user_id = s.user_id
    LEFT JOIN
        courses AS c
    ON
        c.id = uc.course_id;
    """
    result_proxy = db.engine.execute(query).fetchall()
    if result_proxy:
        data = [dict(row) for row in result_proxy]
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
    return "Success"


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
