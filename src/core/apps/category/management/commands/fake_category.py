from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker

from apps.category.models.models import Category


class Command(BaseCommand):
    help = "Generate Fake Category data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            help="Export data to JSON format for cross-database use",
        )

    def handle(self, *args, **options):
        count = options.get("count")
        count = count if count else 10
        fake_en = Faker()
        fake_fa = Faker(locale="fa_IR")
        for _ in range(count):
            title_en = fake_en.word()
            title_fa = fake_fa.word()
            Category.objects.create(
                title_en=title_en,
                title_fa=title_fa,
                description_en=fake_en.paragraph(nb_sentences=5),
                description_fa=fake_fa.paragraph(nb_sentences=5),
                sort_order=fake_en.random_number(digits=2),
                slug=slugify(title_fa, allow_unicode=True),
            )

        self.stdout.write(
            self.style.SUCCESS("\nSuccessfully created ")
            + self.style.ERROR(count)
            + self.style.SUCCESS(" category data.")
        )
