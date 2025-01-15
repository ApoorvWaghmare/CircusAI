class Config(object):
    DEBUG = False
    TESTING = False
    LOCAL_TEMP_STORE = '/home/ubuntu/CircusAI/application/backend/ai_engine/medias'
    CLOUDFRONT_SETTINGS = {
        'private_key': '/home/ubuntu/CircusAI/application/docs/privateCircusAICloudFront.pem',
        'key_pair_id': 'K3ELQD9A1KMYL5',
        'domain_name': 'https://d17lf0z4884e4u.cloudfront.net',
        'url_expiry_hrs': 24,
        'local_storage_folder': './medias/'
    }
    S3_SETTINGS = {
        'aws_access_key_id': 'AKIA3FLDXHDBBXYST7VN',
        'aws_secret_access_key': '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',
        'bucket_name': 'circusaivirginiabuck'
    }
    SNS_SETTINGS = {
        'region': 'us-east-1',
        'topic_arn': 'arn:aws:sns:us-east-1:767397673154:CircusAITopic',
        'aws_access_key_id': 'AKIA3FLDXHDBBXYST7VN',
        'aws_secret_access_key': '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',
        'ios_platform_arn': 'arn:aws:sns:us-east-1:767397673154:app/APNS/CircusAITopicSubiOS',
        'protocol': 'application'
    }

class ProductionConfig(Config):
    pass  # additional production-specific settings

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True