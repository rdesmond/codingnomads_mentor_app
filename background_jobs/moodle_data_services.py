import requests
from .config import MOODLE_API_URL


def get_all_users():
    users = requests.get(f'{MOODLE_API_URL}/api/users')
    if users.status_code != 200:
        return None
    return users.json()


def get_user_by_id(id):
    user = requests.get(f'{MOODLE_API_URL}/api/users/{id}')
    if user.status_code != 200:
        return None
    return user.json()


def get_all_students():
    students = requests.get(f'{MOODLE_API_URL}/api/students')
    if students.status_code != 200:
        return None
    return students.json()


def get_student_by_id(id):
    student = requests.get(f'{MOODLE_API_URL}/api/students/{id}')
    if student.status_code != 200:
        return None
    return student.json()


def get_all_mentors():
    mentors = requests.get(f'{MOODLE_API_URL}/api/mentors')
    if mentors.status_code != 200:
        return None
    return mentors.json()


def get_mentor_by_id(id):
    mentor = requests.get(f'{MOODLE_API_URL}/api/mentors/{id}')
    if mentor.status_code != 200:
        return None
    return mentor.json()


def get_all_courses():
    courses = requests.get(f'{MOODLE_API_URL}/api/courses')
    if courses.status_code != 200:
        return None
    return courses.json()


def get_student_progress(id):
    progress = requests.get(f'{MOODLE_API_URL}/api/students/{id}/progress')
    if progress.status_code != 200:
        return None
    return progress.json()


def get_student_activity(id):
    activity = requests.get(f'{MOODLE_API_URL}/api/students/{id}/activity-log')
    if activity.status_code != 200:
        return None
    return activity.json()
