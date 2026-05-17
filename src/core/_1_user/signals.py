from django.db.models.signals import post_save
from django.dispatch import receiver

from _1_user._modules.user_setting.views.base.views import (
    get_user_setting_objects,
)
from _1_user.models.models import User
from apps.wallet.views.base.views import get_wallet_objects


@receiver(post_save, sender=User)
def create_setting(sender, instance, created, **kwargs):
    if created:
        get_user_setting_objects().create(user=instance)


@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        get_wallet_objects().create(user=instance)
