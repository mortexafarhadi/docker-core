from django.db import models

from _0_utils.models import basic_models as mb
from _0_utils.templatetags.poll_extras import separate_with_dash
from apps.wallet.models.models import Wallet


class WalletCard(mb.BasicModelHistorical):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    shaba_number = models.CharField(max_length=100, null=True, blank=True)
    is_main = models.BooleanField(default=False)
    bank_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return separate_with_dash(self.card_number)
