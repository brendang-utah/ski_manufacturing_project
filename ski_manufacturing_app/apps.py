from django.apps import AppConfig


class SkiManufacturingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ski_manufacturing_app'
    def ready(self):
        import ski_manufacturing_app.signals