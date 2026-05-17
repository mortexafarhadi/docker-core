from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "_2_account"

    def ready(self):
        import _2_account.signals
