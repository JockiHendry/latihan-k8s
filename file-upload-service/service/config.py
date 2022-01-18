import os


class Config:
    ENABLE_RABBITMQ = True
    RABBITMQ_HOST = 'localhost'
    RABBITMQ_PORT = '5672'
    RABBITMQ_USER = 'user'
    RABBITMQ_PASSWORD = 'password'
    MAX_CONTENT_LENGTH = 50_000_000
    UPLOAD_FOLDER = '/uploads'


class TestingConfig(Config):
    ENABLE_RABBITMQ = False
    UPLOAD_FOLDER = '/tmp/uploads'


class DevelopmentConfig(Config):
    UPLOAD_FOLDER = '/tmp/uploads'


class ProductionConfig(Config):
    RABBITMQ_HOST = 'rabbitmq'
    RABBITMQ_USER = os.environ.get('RABBITMQ_USER')
    RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD')
