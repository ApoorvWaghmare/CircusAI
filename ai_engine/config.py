class Config(object):
    pass

class ProductionConfig(Config):
    pass  # additional production-specific settings

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True