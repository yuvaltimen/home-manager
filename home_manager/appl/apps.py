from django.apps import AppConfig


class ShoppingListConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appl'

    def ready(self):
        import appl.signals
