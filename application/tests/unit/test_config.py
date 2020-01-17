import os


def test_development_config(test_app):
    test_app.config.from_object('application.config.DevelopmentConfig')
    assert test_app.config['SECRET_KEY'] == '12345'
    assert not test_app.config['TESTING']
    assert test_app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_URL')


def test_testing_config(test_app):
    test_app.config.from_object('application.config.TestingConfig')
    assert test_app.config['SECRET_KEY'] == '12345'
    assert test_app.config['TESTING']
    assert not test_app.config['PRESERVE_CONTEXT_ON_EXCEPTION']
    assert test_app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_TEST_URL')


def test_production_config(test_app):
    test_app.config.from_object('application.config.ProductionConfig')
    assert test_app.config['SECRET_KEY'] == '12345'
    assert not test_app.config['TESTING']
    assert test_app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_URL')