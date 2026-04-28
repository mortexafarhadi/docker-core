from django.core.management.base import BaseCommand

from __user.views.base.views_user import get_user_model


class Command(BaseCommand):
    help = "Creates a superuser if it doesn't exist"

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            user = User.objects.create_superuser(
                username="admin", phone="9123456789", email="admin@admin.com"
            )
            user.set_password("123")
            user.save()
            self.stdout.write(self.style.SUCCESS("✅ Superuser created."))
        else:
            self.stdout.write(self.style.WARNING("ℹ️ Superuser already exists."))
