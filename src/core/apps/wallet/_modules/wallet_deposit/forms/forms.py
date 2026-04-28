from django import forms

from ..models import models as mm


class WalletDepositForm(forms.ModelForm):
    class Meta:
        model = mm.WalletDeposit
        fields = ["amount"]
        widgets = {
            "amount": forms.NumberInput(
                attrs={"class": "form-control fs-5", "required": True}
            ),
        }
