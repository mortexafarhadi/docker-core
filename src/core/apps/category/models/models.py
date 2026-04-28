from django.db import models
from django.urls import reverse
from translated_fields import TranslatedField

from ___utils.functions.generator import uniq_slugify as tc
from ___utils.functions.generator.url_image_base import get_image_thumbnail
from ___utils.functions.string_function import to_kebab_case
from ___utils.models import basic_models as mb
from ___utils.models import mixin_models as mx


class Category(mb.BaseCKEditorMultiLangModelActiveSortOrderHistorical, mx.SlugMixin):
    title = TranslatedField(models.CharField(max_length=200, default=""))
    image = models.ImageField(upload_to="images/Category/", null=True, blank=True)
    alt_image_name = models.CharField(max_length=200, null=True, blank=True)

    def set_slug(self):
        self.slug = tc.uniq_slugify_slug_safe_dash(self, to_kebab_case(self.title))

    def save(self, *args, **kwargs):
        if not self.is_deleted:
            if not self.slug or self.slug is None:
                self.set_slug()
            super().save(*args, **kwargs)

    def get_image_tmb_url(self):
        return get_image_thumbnail(self.image)

    def get_admin_detail_v1_url(self):
        return reverse("admin-v1-category:detail", kwargs={"pk": self.pk})

    def get_admin_update_v1_url(self):
        return reverse("admin-v1-category:edit", kwargs={"pk": self.pk})

    def get_admin_detail_v2_url(self):
        return reverse("admin-v2-category:detail", kwargs={"pk": self.pk})

    def get_admin_update_v2_url(self):
        return reverse("admin-v2-category:edit", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title
