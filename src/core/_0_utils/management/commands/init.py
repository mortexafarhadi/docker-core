from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Runs initial setup and optionally creates migrations"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting setup..."))

        self.stdout.write(self.style.SUCCESS("\n🛠 Creating new migrations..."))
        call_command("makemigrations")

        # اجرای میگریشن‌ها
        self.stdout.write(self.style.SUCCESS("\nApplying migrations..."))
        call_command("migrate")

        # اجرای دستور ساخت ادمین
        self.stdout.write(self.style.SUCCESS("\nSetting up admin..."))
        call_command("setup_admin")
        call_command("setup_test_user")

        self.stdout.write(self.style.SUCCESS("\n\n🚀 Project is ready to go!"))
