from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from ..models.models import UserSocialMedia
from __user.views.base.views_user import get_users_all
from apps.social_network.views.base.views import get_social_networks_all


class UserSocialMediaForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        required=True,
        queryset=get_users_all().order_by("-date_joined"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    social_network = forms.ModelChoiceField(
        required=True,
        queryset=get_social_networks_all().order_by("-datetime_create"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = UserSocialMedia
        exclude = [
            "is_deleted",
            "datetime_create",
            "datetime_update",
            "datetime_delete",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control fs-5", "required": True}
            ),
            "sort_order": forms.NumberInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "description": CKEditor5Widget(),
        }
