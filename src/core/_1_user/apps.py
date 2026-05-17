from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "_1_user"

    def ready(self):
        import _1_user.signals
