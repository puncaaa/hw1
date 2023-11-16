from django.apps import AppConfig

class NewstableConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newstable'

    def ready(self):
        import newstable.signals
