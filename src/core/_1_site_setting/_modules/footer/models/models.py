from django.db import models
from django.urls import reverse

from _0_utils.models import basic_models as mb


class FooterLinkGroup(mb.BaseCKEditorModelActiveSortOrderHistorical):
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
    title = models.CharField(max_length=200)
    link = models.URLField(null=True, blank=True)
    open_in_newtab = models.BooleanField(default=False)
    is_move_mode = models.BooleanField(default=True)
    move_target_id = models.CharField(max_length=200, null=True, blank=True)
    has_child = models.BooleanField(default=False)

    def get_open_in_newtab(self):
        return "On" if self.open_in_newtab else "Off"

    def get_is_move_mode(self):
        return "On" if self.is_move_mode else "Off"

    def get_has_child(self):
        return "On" if self.has_child else "Off"

    def get_admin_detail_v1_url(self):
        return reverse("admin-v1-setting-footer-group-detail", kwargs={"pk": self.pk})

    def get_admin_update_v1_url(self):
        return reverse("admin-v1-setting-footer-group-edit", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


class FooterLink(mb.BaseCKEditorModelActiveSortOrderHistorical):
    group = models.ForeignKey(
        FooterLinkGroup, on_delete=models.CASCADE, related_name="parent"
    )
    title = models.CharField(max_length=200)
    link = models.URLField(null=True, blank=True)
    open_in_newtab = models.BooleanField(default=False)

    def get_open_in_newtab(self):
        return "On" if self.open_in_newtab else "Off"

    def get_admin_detail_v1_url(self):
        return reverse("admin-v1-setting-footer-link-detail", kwargs={"pk": self.pk})

    def get_admin_update_v1_url(self):
        return reverse("admin-v1-setting-footer-link-edit", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title
