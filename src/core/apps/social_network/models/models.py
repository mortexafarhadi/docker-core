from django.db import models
from django.urls import reverse

from ___utils.functions.generator.url_image_base import get_image_thumbnail
from ___utils.models import basic_models as mb


class SocialNetwork(mb.BaseCKEditorModelActiveSortOrderHistorical):
    title = models.CharField(max_length=200)
    link = models.URLField()
    icon_name = models.CharField(max_length=250, blank=True, null=True)
    image = models.ImageField(upload_to="images/social_network/", null=True, blank=True)

    def get_image_tmb_url(self):
        return get_image_thumbnail(self.image)

    def get_admin_detail_v1_url(self):
        return reverse("admin-v1-social-network:detail", kwargs={"pk": self.pk})

    def get_admin_update_v1_url(self):
        return reverse("admin-v1-social-network:edit", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title
