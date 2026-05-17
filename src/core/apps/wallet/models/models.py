from django.db import models

from _2_account.views.base.views_user import get_user_model
from _0_utils.models import mixin_models as mx

User = get_user_model()


class Wallet(mx.UUIDMixin, mx.DatetimeUpdateMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # # for rial
    balance = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    pending = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    locked = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    # # for euro
    # balance = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    # pending = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    # locked = models.DecimalField(max_digits=15, decimal_places=3, default=0)

    def get_available_balance(self):
        """Returns the balance that is not locked."""
        # موجودی قابل استفاده = بالانس کل - مبلغ قفل شده
        return self.balance - self.locked

    def get_total_balance(self):
        """Returns the total balance including pending amounts."""
        # موجودی کل = بالانس اصلی + مبلغ در انتظار تایید
        return self.balance + self.pending

    def get_latest_transactions(self, count=10):
        """
        Retrieves the latest deposit and withdrawal transactions for this wallet.

        Args:
            count (int): The maximum number of transactions to return. Defaults to 10.

        Returns:
            list: A list of the most recent WalletDeposit and WalletWithdrawal objects,
                  sorted by creation date in descending order.
        """
        latest_deposits = self.deposits.filter(wallet=self).order_by(
            "-datetime_create"
        )[:count]
        latest_withdrawals = self.withdrawals.filter(wallet=self).order_by(
            "-datetime_create"
        )[:count]

        all_transactions = list(latest_deposits) + list(latest_withdrawals)
        all_transactions.sort(key=lambda x: x.datetime_create, reverse=True)

        return all_transactions[:count]

    def __str__(self):
        return f"w-{self.user} ({self.balance})"
