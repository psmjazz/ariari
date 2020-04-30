import os


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.urandom(8)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OAUTHLIB_INSECURE_TRANSPORT = False


class ProdConfig(Config):
    ENV = 'production'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://sam:z748159!@localhost:3306/prod_db?charset=utf8'


class DevConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://sam:z748159!@localhost:3306/dev_db?charset=utf8'
    GOOGLE_OAUTH2_CLIENT_SECRETS_FILE = 'C:\\Users\\khtks\\PycharmProjects\\vacation_management\\application\\credentials.json'


class TestConfig(Config):
    ENV = 'testing'
    TESTING = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://sam:z748159!@localhost:3306/test_db?charset=utf8'


config_name = dict(
    prod=ProdConfig,
    dev=DevConfig,
    test=TestConfig
)