from django.apps import AppConfig

class MongoDBConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.mongodb'
    verbose = 'mongodb app'

    def ready(self):
        try:
            from .services import StartUpService
            StartUpService.global_init()
        except Exception as e:
            print(e)