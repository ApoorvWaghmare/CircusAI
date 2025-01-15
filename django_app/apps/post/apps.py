from django.apps import AppConfig

class PostConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.post'
    verbose = 'post app'

    def ready(self):
        import apps.post.signals 