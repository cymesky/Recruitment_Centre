from django.apps import AppConfig


class WebsiteAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website_app'

    def ready(self):
        from . import updater
        updater.start()
