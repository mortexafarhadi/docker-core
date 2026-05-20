from django.db import models, transaction
from django.urls import reverse

from _0_utils.functions.date_and_time_function import now
from _0_utils.models import mixin_models as mx
from apps.wallet._modules.wallet_card.models.models import WalletCard
from apps.wallet.models.models import Wallet


class WalletWithdrawal(
    mx.UUIDMixin, mx.TimeStampedMixin, mx.DescriptionMixin, mx.HistoricalMixin
):
    class StatusChoices(models.TextChoices):
        REQUEST = "request", "Request"
        REJECTED = "rejected", "Rejected"
        IN_PAYMENT_QUEUE = "in_payment_queue", "In Payment Queue"
        USER_CANCELED = "user_canceled", "User Canceled"
        COMPLETED = "completed", "Completed"
        # Order (Use Customer Wallet Balance)
        PAYMENT_ERROR = "payment_error", "Payment Error"

    STATUS_COLOR_MAP = {
        "request": "warning",
        "rejected": "danger",
        "in_payment_queue": "primary",
        "processing": "primary",
        "user_canceled": "secondary",
        "completed": "success",
        "payment_error": "danger",
    }

    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="withdrawals"
    )
    wallet_card = models.ForeignKey(
        WalletCard,
        on_delete=models.SET_NULL,
        related_name="withdrawals",
        null=True,
        blank=True,
    )
    # amount = models.DecimalField(max_digits=27, decimal_places=2, default=0)  # Euro - Dollar
    amount = models.DecimalField(
        max_digits=15, decimal_places=0, default=0
    )  # Toman - Rial
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.REQUEST,
    )
    datetime_complete = models.DateTimeField(null=True, blank=True)
    datetime_process = models.DateTimeField(null=True, blank=True)
    datetime_cancel = models.DateTimeField(null=True, blank=True)
    datetime_reject = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True, null=True)

    def get_user(self):
        return self.wallet.user

    @transaction.atomic
    def request_withdrawal(self, amount_to_withdraw):
        if amount_to_withdraw <= 0:
            raise ValueError("مبلغ برداشت باید مثبت باشد.")

        available_balance = self.wallet.balance
        if amount_to_withdraw > available_balance:
            raise ValueError("موجودی کافی برای این برداشت وجود ندارد.")

        self.wallet.balance -= amount_to_withdraw
        self.wallet.locked += amount_to_withdraw
        self.wallet.save(update_fields=["balance", "locked", "datetime_update"])

        self.amount = amount_to_withdraw
        self.status = self.StatusChoices.REQUEST

    @transaction.atomic
    def set_rejected(self, rejection_reason=""):
        if self.status not in [
            self.StatusChoices.REQUEST,
            self.StatusChoices.IN_PAYMENT_QUEUE,
        ]:
            raise ValueError(f"برداشت در وضعیت '{self.status}' است و قابل رد شدن نیست.")

        self.wallet.locked -= self.amount
        if self.wallet.locked < 0:
            self.wallet.locked = 0

        self.wallet.balance += self.amount
        self.wallet.save(update_fields=["balance", "locked", "datetime_update"])

        self.status = self.StatusChoices.REJECTED
        self.datetime_reject = now()
        self.rejection_reason = rejection_reason

    @transaction.atomic
    def set_payment_error(self, reason=""):
        if self.status != [
            self.StatusChoices.REQUEST,
            self.StatusChoices.IN_PAYMENT_QUEUE,
        ]:
            raise ValueError(f"برداشت در وضعیت '{self.status}' است و قابل لغو نیست.")

        self.wallet.locked -= self.amount
        if self.wallet.locked < 0:
            self.wallet.locked = 0

        self.wallet.balance += self.amount
        self.wallet.save(update_fields=["balance", "locked", "datetime_update"])

        self.status = self.StatusChoices.PAYMENT_ERROR
        self.datetime_complete = now()
        self.rejection_reason = reason

    @transaction.atomic
    def set_user_canceled(self, reason=""):
        if self.status != self.StatusChoices.REQUEST:
            raise ValueError(f"برداشت در وضعیت '{self.status}' است و قابل لغو نیست.")

        self.wallet.locked -= self.amount
        if self.wallet.locked < 0:
            self.wallet.locked = 0

        self.wallet.balance += self.amount
        self.wallet.save(update_fields=["balance", "locked", "datetime_update"])

        self.status = self.StatusChoices.USER_CANCELED
        self.datetime_cancel = now()
        self.rejection_reason = reason

    @transaction.atomic
    def set_completed(self):
        if self.status != self.StatusChoices.IN_PAYMENT_QUEUE:
            raise ValueError(f"برداشت در وضعیت '{self.status}' است و قابل تکمیل نیست.")

        self.wallet.locked -= self.amount
        if self.wallet.locked < 0:
            self.wallet.locked = 0

        self.wallet.save(update_fields=["locked", "datetime_update"])

        self.status = self.StatusChoices.COMPLETED
        self.datetime_complete = now()

    @transaction.atomic
    def set_payment_queue(self):
        if self.status != self.StatusChoices.REQUEST:
            raise ValueError(f"برداشت در وضعیت '{self.status}' است و قابل پردازش نیست.")
        self.status = self.StatusChoices.IN_PAYMENT_QUEUE
        self.datetime_process = now()

    def __str__(self):
        return f"w-{self.wallet} - {self.amount} ({self.status})"

    def get_wallet_card(self):
        wallet_card = self.wallet_card
        return (
            f"{wallet_card.card_number}\n{wallet_card.shaba_number}"
            if wallet_card
            else "----"
        )

    def get_status_bg_color(self):
        return self.STATUS_COLOR_MAP.get(self.status, "light")

    def is_status_request(self):
        return True if self.status == self.StatusChoices.REQUEST else False

    def is_status_rejected(self):
        return True if self.status == self.StatusChoices.REJECTED else False

    def is_status_in_payment_queue(self):
        return True if self.status == self.StatusChoices.IN_PAYMENT_QUEUE else False

    def is_status_user_canceled(self):
        return True if self.status == self.StatusChoices.USER_CANCELED else False

    def is_status_completed(self):
        return True if self.status == self.StatusChoices.COMPLETED else False

    def get_admin_detail_v1_url(self):
        return reverse(
            "admin-v1-user-wallet-withdrawal:detail",
            kwargs={"user_code": self.wallet.user.code, "pk": self.pk},
        )
