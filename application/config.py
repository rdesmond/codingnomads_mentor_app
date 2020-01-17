import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '12345'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # # postgres
    # db_user = os.environ.get('DB_USER', 'postgres')
    # db_host = os.environ.get('DB_HOST', 'localhost')
    # db_name = os.environ.get('DB_NAME', 'mentor_portal')

    # db_password = os.environ.get('DB_PASSWORD', 'password')
    # # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=db_user,pw=db_password,url=db_host,db=db_name)



class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')