import os
from datetime import datetime

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from ___utils.base_variables import BASE_DIR


class Command(BaseCommand):
    help = "Backups database (SQLite file or JSON data)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--data",
            action="store_true",
            help="Export data to JSON format for cross-database use",
        )

    def handle(self, *args, **options):
        backup_dir = os.path.join(BASE_DIR, "__data")
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        if options["data"]:
            # خروجی JSON برای انتقال بین دیتابیس‌ها
            file_path = os.path.join(backup_dir, f"data_backup_{now}.json")
            self.stdout.write(self.style.HTTP_INFO("Creating JSON dump..."))
            with open(file_path, "w", encoding="utf-8") as f:
                call_command(
                    "dumpdata",
                    natural_primary=True,
                    natural_foreign=True,
                    indent=2,
                    exclude=["contenttypes", "auth.Permission", "sessions"],
                    stdout=f,
                )
            self.stdout.write(self.style.SUCCESS(f"✅ Data dumped to {file_path}"))
        else:
            # کپی فایل دیتابیس (مخصوص SQLite)
            import shutil

            db_path = settings.DATABASES["default"]["NAME"]
            destination = os.path.join(backup_dir, f"db_backup_{now}.sqlite3")
            shutil.copy2(db_path, destination)
            self.stdout.write(
                self.style.SUCCESS(f"✅ Database file copied to {destination}")
            )
