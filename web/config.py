import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    LOGGING_TO_FILE = 'logs.log'
    LOGGING_LEVEL = logging.DEBUG
    LOGGING_TO_KAFKA_HOST = "localhost:9092"
    LOGGING_TO_KAFKA_TOPIC = "test"
    LOGGING_FORMAT = '{"sourceApp": "%(name)s", "messageType": "Log", "logLevel": "%(levelname)s", ' \
                     '"serverTime": "%(asctime)s", "source": "%(pathname)s: %(lineno)d", "message": "%(message)s"}'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': ProductionConfig,
}
