from django.apps import AppConfig


class WebshocketConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webshocket'

    def ready(self):
        import webshocket.signals