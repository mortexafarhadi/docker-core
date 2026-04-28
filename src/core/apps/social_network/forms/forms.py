from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from ..models import models as mm


class SocialNetworkForm(forms.ModelForm):
    clear_image = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = mm.SocialNetwork
        exclude = [
            "is_deleted",
            "datetime_create",
            "datetime_update",
            "datetime_delete",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control fs-5", "required": True}
            ),
            "link": forms.URLInput(
                attrs={"class": "form-control fs-5", "required": True}
            ),
            "icon_name": forms.TextInput(
                attrs={"class": "form-control fs-5", "required": False}
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "required": False,
                }
            ),
            "sort_order": forms.NumberInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "description": CKEditor5Widget(),
        }
