class Config(object):
    DEBUG = False
    TESTING = False
    MONGODB_SETTINGS = {
        'host': 'mongodb+srv://apoorvwaghmare:YrAwIHXFYSUrV7e2@cluster0.aza6080.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0',
        'db': 'circus_ai_mongo_db'
    }
    # other global settings

class ProductionConfig(Config):
    pass  # additional production-specific settings

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True