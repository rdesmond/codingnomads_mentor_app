from application.models import User, UserPreferences


def test_add_user_preferences(test_app, test_database, add_user):
    user = add_user('jonny')
    user_preferences = UserPreferences(user_id = user.id)
    test_database.session.add(user_preferences)
    test_database.session.commit()


    assert user.preferences.monday == False
    assert user_preferences.user_id == user.id
