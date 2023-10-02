from os import environ

class Config:
    FLASK_PORT=8080
    DEBUG=False
    TESTING=False
    QUEUE_NAME='reconstruction'
    REDIS_HOST=environ.get('REDIS_HOST')
    REDIS_PORT=6379
    REDIS_URL=environ.get('REDIS_URL')
    QUEUE_JOB_TIMEOUT=1800

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG=True

class TestingConfig(Config):
    TESTING=True