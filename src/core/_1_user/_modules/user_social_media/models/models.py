from django.db import models

from _0_utils.models import basic_models as mb
from apps.social_network.models.models import SocialNetwork
from _1_user.models import models as mu


class UserSocialMedia(mb.BaseCKEditorModelActiveSortOrderHistorical):
    user = models.ForeignKey(mu.User, on_delete=models.CASCADE)
    social_network = models.ForeignKey(SocialNetwork, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)

    def get_social_media_link(self):
        return f"{self.social_network.link}/{self.username}"

    def __str__(self):
        return f"{self.user} - {self.social_network} : {self.username}"
