from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from _2_locales import errors_fa, placeholder_en, placeholder_fa, errors_en

Email = placeholder_en.Email
Email_fa = placeholder_fa.Email
CurrentPassword = placeholder_en.CurrentPassword
CurrentPassword_fa = placeholder_fa.CurrentPassword
Password = placeholder_en.Password
Password_fa = placeholder_fa.Password
FirstName = "First Name"
LastName = "Last Name"
ConfirmPassword = placeholder_en.ConfirmPassword
ConfirmPassword_fa = placeholder_fa.ConfirmPassword
error_password_confirm_password_not_correct = (
    errors_en.password_confirm_password_not_correct
)
error_password_confirm_password_not_correct_fa = (
    errors_fa.password_confirm_password_not_correct
)


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": FirstName,
                "autofocus": True,
            }
        ),
        required=True,
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": LastName}
        ),
        required=True,
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": Email}),
        validators=[
            validators.EmailValidator,
        ],
        required=True,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": Password}
        ),
        required=True,
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": ConfirmPassword}
        ),
        required=True,
    )

    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(),required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget.attrs["id"] = "checkstrength"

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if confirm_password == password:
            return password
        else:
            raise ValidationError(error_password_confirm_password_not_correct)


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": Email,
                "autofocus": True,
            }
        ),
        validators=[
            validators.EmailValidator,
        ],
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": Password}
        )
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(), required=True)


class ForgetPassForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": Email,
                "autofocus": True,
            }
        ),
        validators=[
            validators.EmailValidator,
        ],
    )
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(), required=True)


class AccountActivationForm(forms.Form):
    activation_code = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Activation Code"}
        ),
    )
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(), required=True)


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": Password}
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": ConfirmPassword}
        )
    )

    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(), required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget.attrs["id"] = "checkstrength"

    def clean_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if confirm_password == password:
            return password
        else:
            raise ValidationError(error_password_confirm_password_not_correct)
