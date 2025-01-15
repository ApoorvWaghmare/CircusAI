class Config(object):
    DEBUG = False
    TESTING = False
    AI_ENGINE_POLLING_DURATION = 500 # seconds
    CUSTOM_AI_ENGINE_SETTINGS = {
        'text_2_image_api': "http://127.0.0.1:5000/ai_engine/app/text-2-image",
        'text_image_2_image_api': "http://127.0.0.1:5000/ai_engine/app/text-image-2-image"
    }
    COMFYUI_AI_ENGINE_SETTINGS = {
        'prompt_api': "http://127.0.0.1:8188/prompt",
        'queue_history_api': 'http://127.0.0.1:8188/history',
        'output_directory': '/home/ubuntu/CircusAI/application/backend/ai_engine/ComfyUI/output',
        'input_directory': '/home/ubuntu/CircusAI/application/backend/ai_engine/ComfyUI/input',
        'seed_min': 0,
        'seed_max': 999999999999999,
        'text_2_image_api_body_path': '/home/ubuntu/CircusAI/application/backend/ai_engine/ComfyUI/workflows/flux-text2image-api.json',
        'text_image_2_image_api_body_path': '/home/ubuntu/CircusAI/application/backend/ai_engine/ComfyUI/workflows/image-text2image-api.json',
        'text_face_2_image_api_body_path': '/home/ubuntu/CircusAI/application/backend/ai_engine/ComfyUI/workflows/face-text2image-api.json'
    }
    MEDIA_TAGGING_AI_ENGINE_HOST = 'http://34.207.59.152:8000'
    MEDIA_TAGGING_AI_ENGINE_SETTINGS = {
        'genre_api': MEDIA_TAGGING_AI_ENGINE_HOST + '/genre',
        'subject_api': MEDIA_TAGGING_AI_ENGINE_HOST + '/subject',
        'mood_api': MEDIA_TAGGING_AI_ENGINE_HOST + '/mood',
        'color_api': MEDIA_TAGGING_AI_ENGINE_HOST + '/color',
        'style_api': MEDIA_TAGGING_AI_ENGINE_HOST + '/style',
        'theme_api': MEDIA_TAGGING_AI_ENGINE_HOST + '/theme',
        'composition_api': MEDIA_TAGGING_AI_ENGINE_HOST + '/composition',
        'location_api': MEDIA_TAGGING_AI_ENGINE_HOST + '/location',
        'medium_api': MEDIA_TAGGING_AI_ENGINE_HOST + '/medium',
    }

class ProductionConfig(Config):
    pass  # additional production-specific settings

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True