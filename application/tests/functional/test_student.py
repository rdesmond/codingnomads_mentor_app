import application.data_services


def test_get_student(test_app, add_user, monkeypatch):
    def mock_get_student_info(student_id):
        data = {
        "student": {
            "aims": "wants to learn to frontend",
            "id": 2,
            "mentor_id": 3,
            "mentor_name": "Gilad Gressel",
            "preferred_learning": "discussions",
            "start_date": "Fri, 13 Sep 2019 13:14:57 GMT",
            "status": "student",
            "user_id": 2,
            "username": "johnny",
            "email": "johnny@gmail.com",
            "first_name": "Carol",
            "last_name": "Dunlop",
            "learning_platform": "carol",
            "forum": "carol",
            "slack": "apple",
            "time_zone": "Europe/London",
            "courses": [
                {
                    "id": 8,
                    "name": "Python Software Development",
                    "progress_percent": 80
                }
            ],
            "preferred_days": {
                "Mon": True, "Tue": True, "Wed": True,
                "Thu": True, "Fri": True, "Sat": True, "Sun": True},
            "preferred_start_time": "08:00",
            "preferred_end_time": "12:00"
            }
        }
        return data

    monkeypatch.setattr(application.blueprints.student, "get_student_info", mock_get_student_info)
    # assert user.username == 'jonny'
    client = test_app.test_client()
    resp = client.get('/student/1')
    assert resp.status_code == 200