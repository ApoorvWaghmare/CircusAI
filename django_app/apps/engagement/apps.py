from django.apps import AppConfig


class EngagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.engagement'
    verbose = 'engagement app'

    def ready(self):
        import apps.engagement.signals 
