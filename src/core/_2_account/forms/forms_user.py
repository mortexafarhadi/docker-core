from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from .. import models as mu


class UserForm(forms.ModelForm):
    clear_avatar = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = mu.User
        fields = [
            "first_name",
            "last_name",
            "username",
            "gender",
            "avatar",
            "description",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control fs-5", "required": False}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control fs-5", "required": False}
            ),
            "username": forms.TextInput(
                attrs={"class": "form-control fs-5", "required": False}
            ),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "avatar": forms.FileInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "required": False,
                }
            ),
            "description": CKEditor5Widget(),
        }
