from django.db import models

from _0_utils.models import basic_models as mb
from apps.social_network.models.models import SocialNetwork


class SiteSocialMedia(mb.BaseCKEditorModelActiveSortOrderHistorical):
    class SITE_TYPES_CHOICES(models.TextChoices):
        MAIN = (
            "main",
            "Main Website / User Panel",
        )
        ADMIN = (
            "admin",
            "Admin Panel",
        )
        LANDING = "landing", "Landing / Introduction"

    site_type = models.CharField(
        max_length=20,
        choices=SITE_TYPES_CHOICES,
        default=SITE_TYPES_CHOICES.MAIN,
        db_index=True,
    )
    social_network = models.ForeignKey(SocialNetwork, on_delete=models.CASCADE)
    open_in_newtab = models.BooleanField(default=True)
    username = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.social_network},{self.username}"
