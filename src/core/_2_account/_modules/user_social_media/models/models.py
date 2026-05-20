from django.db import models

from _0_utils.models import basic_models as mb
from apps.social_network.models.models import SocialNetwork
from _2_account.models.models import User


class UserSocialMedia(mb.BaseCKEditorModelActiveSortOrderHistorical):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="social_medias"
    )
    social_network = models.ForeignKey(SocialNetwork, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)

    def get_link(self):
        return f"{self.social_network.link}/{self.username}"

    def __str__(self):
        return f"{self.user} - {self.social_network} : {self.username}"
