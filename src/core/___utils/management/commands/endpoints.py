from django.core.management.base import BaseCommand
from django.urls import get_resolver, URLResolver


class Command(BaseCommand):
    help = "Displays URLs grouped by module. Usage: endpoints [module1 module2 ...]"

    def add_arguments(self, parser):
        # دریافت نام ماژول‌ها به صورت اختیاری
        parser.add_argument(
            "modules", nargs="*", type=str, help="Filter by module names"
        )

    def handle(self, *args, **options):
        urlconf = get_resolver(None)
        target_modules = [m.lower() for m in options["modules"]]
        self.print_urls(urlconf.url_patterns, target_modules=target_modules)

    def print_urls(self, patterns, prefix="", last_module="", target_modules=None):
        for pattern in patterns:
            current_module = ""

            # استخراج ایمن نام ماژول
            if hasattr(pattern, "callback") and pattern.callback:
                current_module = pattern.callback.__module__.split(".")[0]
            elif isinstance(pattern, URLResolver):
                # اگر رشته بود (مثل 'app.urls')، اگر نه که خود شیء را بررسی کن
                module_str = str(pattern.urlconf_name)
                current_module = module_str.split(".")[0]

            # فیلتر کردن بر اساس ماژول‌های ورودی (اگر کاربر ماژولی وارد کرده باشد)
            if target_modules and current_module.lower() not in target_modules:
                if isinstance(pattern, URLResolver):  # برای پیمایش زیرمجموعه‌ها
                    self.print_urls(
                        pattern.url_patterns,
                        prefix + str(pattern.pattern),
                        last_module,
                        target_modules,
                    )
                continue

            # نمایش هدر ماژول
            if current_module and current_module != last_module:
                self.stdout.write(
                    self.style.MIGRATE_LABEL(f"\n📦 MODULE: {current_module.upper()}")
                )
                self.stdout.write(self.style.HTTP_INFO("-" * 45))
                last_module = current_module

            if isinstance(pattern, URLResolver):
                self.print_urls(
                    pattern.url_patterns,
                    prefix + str(pattern.pattern),
                    last_module,
                    target_modules,
                )
            else:
                full_url = prefix + str(pattern.pattern)
                # تمیز کردن نمایش URL
                full_url = full_url.replace("^", "").replace("$", "")
                name = f" [{pattern.name}]" if pattern.name else ""
                self.stdout.write(
                    f"  {self.style.SUCCESS('➜')} {full_url:<40} {self.style.WARNING(name)}"
                )
