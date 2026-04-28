from django import forms

from ..models import models as mm
from ...wallet_card.views.base.views import (
    get_wallet_card_none,
    get_wallet_cards_with_wallet,
)


class WalletWithdrawalForm(forms.ModelForm):
    wallet_card = forms.ModelChoiceField(
        queryset=get_wallet_card_none(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        # دریافت والت که در متد __init__ فیلتر شده بود
        wallet_card = self.cleaned_data.get("wallet_card")

        if wallet_card and amount:
            wallet = wallet_card.wallet
            if amount > wallet.balance:
                raise forms.ValidationError(
                    f"موجودی کافی نیست. موجودی فعلی شما {wallet.balance} می‌باشد."
                )

        if amount <= 0:
            raise forms.ValidationError("مبلغ باید بیشتر از صفر باشد.")

        return amount

    class Meta:
        model = mm.WalletWithdrawal
        fields = ["wallet_card", "amount"]
        widgets = {
            "amount": forms.NumberInput(
                attrs={"class": "form-control fs-5", "required": True}
            ),
        }

    def __init__(self, *args, **kwargs):
        wallet = kwargs.pop("wallet", None)
        super().__init__(*args, **kwargs)

        if wallet:
            self.fields["wallet_card"].queryset = get_wallet_cards_with_wallet(
                wallet=wallet
            )
