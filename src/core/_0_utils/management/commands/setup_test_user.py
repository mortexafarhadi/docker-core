from django.core.management.base import BaseCommand
from django.db.models import Q

from _2_account.views.base.views_user import get_user_model


class Command(BaseCommand):
    help = "Creates a test user if it doesn't exist"

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(
            Q(username__iexact="test") | Q(email__iexact="test@test.com")
        ).exists():
            user = User.objects.create_superuser(
                username="test", phone_number="9987654321", email="test@test.com"
            )
            user.set_password("123")
            user.save()
            self.stdout.write(self.style.SUCCESS("✅ Test User created."))
        else:
            self.stdout.write(self.style.WARNING("ℹ️ Test User already exists."))
