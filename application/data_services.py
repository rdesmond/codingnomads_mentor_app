from . import db
from .models import User, Student, Course, SupportLog, Mentor


def get_student_info(id):

    data = None

    student = Student.query.filter(Student.id == id).first()
    if student:
        data = student.to_dict()
    
    return data


def get_mentor_info(id):

  data = None

  mentor = Mentor.query.filter(Mentor.id == id).first()

  if mentor:
    data = mentor.to_dict()
  
  return data


def log_student_support(
    mentor_id, 
    student_id, 
    support_type, 
    time_spent, 
    notes, 
    comprehension):

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

  return 'support successfully added'


def get_student_support_logs(mentor_id, student_id):

  logs = SupportLog.query.filter(SupportLog.mentor_id==mentor_id).filter(SupportLog.student_id==student_id).all()

  if logs:
    data = [log.to_dict() for log in logs]
  else:
    data = None

  return data


def get_student_overview(id):
    # TODO: what was this call about? seems to get info about the student (+some), maybe should be related to mentor?

  data = None

  query = """
  SELECT
    s.user_id
  ,uc.course_id
  ,c.course_name
  FROM
    students AS s
  LEFT JOIN
    user_courses AS uc
  ON
    uc.user_id = s.user_id
  LEFT JOIN
    courses AS c
  ON
    c.id = uc.course_id
  """

  result_proxy = db.engine.execute(query).fetchall()

  if result_proxy:
    data = [dict(row) for row in result_proxy]

  return data
    

def get_all_students():

  data = []

  students = Student.query.all()

  for student in students:
    data.append(student.to_dict())
  
  return data


def assign_students_to_mentor(student_id, mentor_id):
  
  student = Student.query.filter_by(id = student_id).first()

  student.mentor_id = mentor_id

  db.session.commit()

  return "Success"


def get_mentors_and_students():
  
  student_mentors_query = """
  SELECT
    s.user_id AS student_id
  ,u.first_name||' '||u.last_name AS student_name
  ,m.user_id AS mentor_id
  ,um.first_name||' '||um.last_name AS mentor_name
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
    um.id = m.user_id
      """

  student_mentors_proxy = db.engine.execute(text(student_mentors_query)).fetchall()

  data = [dict(row) for row in student_mentors_proxy]

  return data


def get_students_with_courses():

  students_query = """
      SELECT
      s.user_id
    ,u.first_name||' '||u.last_name AS name
    ,uc.course_id
    ,c.course_name
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
        user_id ASC
      """
  students_proxy = db.engine.execute(text(students_query)).fetchall()

  data = [dict(row) for row in students_proxy]

  return data


def get_mentors_with_courses():

  mentors_query = """
    SELECT
      m.user_id
    ,u.first_name||' '||u.last_name AS name
    ,uc.course_id
    ,c.course_name
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
      user_id ASC
    """
  mentors_proxy = db.engine.execute(text(mentors_query)).fetchall()

  data = [dict(row) for row in mentors_proxy]

  return data
