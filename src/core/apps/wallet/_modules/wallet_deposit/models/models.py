from django.db import models, transaction
from django.urls import reverse

from _0_utils.models import mixin_models as mx
from apps.wallet.models.models import Wallet


class WalletDeposit(mx.UUIDMixin, mx.DatetimeCreateMixin, mx.DescriptionMixin):
    class StatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="deposits"
    )
    amount = models.DecimalField(max_digits=27, decimal_places=2, default=0)
    transaction_reference = models.CharField(
        max_length=100, unique=True, blank=True, null=True
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )

    def get_admin_detail_v1_url(self):
        return reverse(
            "admin-v1-user-wallet-deposit:detail",
            kwargs={"user_code": self.wallet.user.code, "pk": self.pk},
        )

    def __str__(self):
        return f"Deposit {self.transaction_reference or self.pk} ({self.amount:.4f}) for {self.wallet.user.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    @transaction.atomic
    def confirm_deposit(self):
        """
        Confirms a deposit, updates wallet balance and pending amount,
        and marks the deposit as completed.
        """
        if self.status == self.StatusChoices.COMPLETED:
            return self
        if self.status == self.StatusChoices.FAILED:
            raise ValueError("این واریز ناموفق بوده است و قابل تایید نیست.")

        if not self.pk:
            self.save()

        # افزودن به pending amount
        self.wallet.pending += self.amount
        self.wallet.save(update_fields=["pending", "datetime_update"])

        self.status = self.StatusChoices.COMPLETED
        # self.save() # save نهایی توسط جنگو انجام میشود
        return self

    @transaction.atomic
    def finalize_deposit(self):
        """
        Finalizes a pending deposit by moving the amount from pending to balance.
        This should be called after confirm_deposit has marked it as completed.
        """
        if self.status != self.StatusChoices.COMPLETED:
            raise ValueError(
                "واریز باید ابتدا تایید (completed) شده باشد تا نهایی شود."
            )
        if self.amount > self.wallet.pending:
            # این حالت نباید رخ دهد اگر منطق درست باشد، اما برای اطمینان
            raise ValueError("مقدار واریز بیشتر از مبلغ در انتظار (pending) است.")

        # کم کردن از pending amount
        self.wallet.pending -= self.amount
        # افزودن به بالانس اصلی
        self.wallet.balance += self.amount
        self.wallet.save(update_fields=["balance", "pending", "datetime_update"])

        # اینجا می توانید وضعیت deposit را به 'finalized' تغییر دهید اگر نیاز دارید
        # self.status = 'finalized'
        # self.save()
        return self

    @transaction.atomic
    def mark_as_failed(self):
        """Marks the deposit as failed. If it was pending, it should be removed from pending."""
        if self.status in [
            self.StatusChoices.COMPLETED,
            self.StatusChoices.FAILED,
        ]:
            return self

        # اگر واریز در حالت pending بود و حالا ناموفق شده، باید از pending کم شود
        if (
            self.status == self.StatusChoices.PENDING
            and self.wallet.pending >= self.amount
        ):
            self.wallet.pending -= self.amount
            self.wallet.save(update_fields=["pending", "datetime_update"])
        # اگر confirm_deposit قبلا فراخوانی شده و به pending اضافه شده،
        # و حالا mark_as_failed فراخوانی شود، باید از pending کم شود.
        # این logic بستگی به workflow دقیق شما دارد.
        # در این پیاده سازی، confirm_deposit به pending اضافه میکند.
        # پس mark_as_failed باید آن را از pending کم کند.

        self.status = self.StatusChoices.FAILED
        self.save()
        return self
