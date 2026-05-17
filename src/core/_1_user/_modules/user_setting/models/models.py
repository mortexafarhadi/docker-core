from django.db import models

from _0_utils.models import basic_models as mb
from _1_user.models import models as mu


class UserSetting(mb.UUIDMixin):
    user = models.OneToOneField(mu.User, on_delete=models.CASCADE)
    language = models.CharField(max_length=100, default="en", null=True, blank=True)
    is_dark_mode = models.BooleanField(default=False)
    background_theme = models.CharField(
        max_length=100, default="bg-default", null=True, blank=True
    )
    color_theme = models.CharField(max_length=100, default="", null=True, blank=True)
    sidebar_mode = models.CharField(
        max_length=100,
        default="adminuiux-sidebar-standard",
        null=True,
        blank=True,
    )

    def get_mode(self):
        return "Dark Mode" if self.is_dark_mode else "Light Mode"

    def __str__(self):
        return f"{self.user} - {self.language},{self.get_mode},{self.background_theme}"
