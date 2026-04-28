import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

# فرض بر این است که BASE_DIR در این مسیر تعریف شده است
from ___utils.base_variables import BASE_DIR


class Command(BaseCommand):
    help = "Sync translations. Use flags like --fa --en or leave empty for all."

    def add_arguments(self, parser):
        # ایجاد فلگ برای هر زبان موجود در تنظیمات پروژه به صورت خودکار
        for lang_code, _ in settings.LANGUAGES:
            parser.add_argument(f"--{lang_code}", action="store_true")

    def handle(self, *args, **options):
        # ۱. تشخیص زبان‌های انتخاب شده توسط کاربر
        selected_languages = [
            lang[0] for lang in settings.LANGUAGES if options.get(lang[0])
        ]

        # اگر هیچ فلگی (مثلاً --fa) زده نشده بود، تمام زبان‌های موجود در تنظیمات را در نظر بگیر
        if not selected_languages:
            selected_languages = [lang[0] for lang in settings.LANGUAGES]

        # ۲. لیست پوشه‌هایی که باید کاملاً نادیده گرفته شوند
        # این کار از بروز UnicodeDecodeError در فایل‌های فونت و استاتیک جلوگیری می‌کند
        ignore_list = [
            "venv/*",
            ".venv/*",
            ".zzvenv/*",
            "env/*",
            "node_modules/*",
            "zstatic/*",
            "static/*",
            "media/*",
            "zmedias/*",
            ".ai/*",
            "___deploy/*",
            "*/fonts/*",
        ]

        self.stdout.write(
            self.style.HTTP_INFO(f"🌐 Syncing translations for: {selected_languages}")
        )

        try:
            # ۳. اطمینان از وجود پوشه locale در ریشه پروژه
            locale_path = os.path.join(BASE_DIR, "locale")
            if not os.path.exists(locale_path):
                os.makedirs(locale_path)
                self.stdout.write(
                    self.style.WARNING(
                        f"📁 Created missing locale directory at {locale_path}"
                    )
                )

            # ۴. استخراج پیام‌ها از کدها (makemessages)
            # استفاده از ignore باعث می‌شود .venv اسکن نشود
            self.stdout.write(self.style.HTTP_INFO("🛠 Running makemessages..."))
            call_command(
                "makemessages",
                locale=selected_languages,
                ignore=ignore_list,
                symlinks=False,
            )

            # ۵. تبدیل فایل‌های متنی .po به فایل‌های باینری .mo (compilemessages)
            # در نسخه‌های جدید جنگو، ignore اینجا هم برای جلوگیری از اسکن مجدد پکیج‌ها موثر است
            self.stdout.write(self.style.HTTP_INFO("⚙️ Running compilemessages..."))
            call_command(
                "compilemessages",
                locale=selected_languages,
                ignore=ignore_list,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Successfully synced and compiled: {', '.join(selected_languages)}"
                )
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error occurred: {str(e)}"))
            self.stdout.write(
                self.style.WARNING("Hint: Ensure 'gettext' is installed on your OS.")
            )
