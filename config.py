import os


class DefaultConfig(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    SECRET_KEY = os.getenv('SECRET_KEY')
    WTF_CSRF_ENABLED = False


class TestDefaultConfig(DefaultConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    TESTING = True
    DEBUG = True
