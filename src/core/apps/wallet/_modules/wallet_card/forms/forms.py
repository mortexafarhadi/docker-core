from django import forms


class WalletCardForm(forms.Form):
    bank_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control fs-5"}),
    )
    card_number = forms.CharField(
        required=True,
        max_length=25,
        widget=forms.TextInput(
            attrs={
                "class": "form-control fs-5",
                "onkeypress": "return isNumberKey(event)",
                "onkeyup": "return setDashForeDigitCard(this)",
            }
        ),
    )
    shaba_number = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control fs-5",
                "onkeypress": "return isNumberKey(event)",
                "onkeyup": "return setDashForeDigitCard(this)",
            }
        ),
    )
